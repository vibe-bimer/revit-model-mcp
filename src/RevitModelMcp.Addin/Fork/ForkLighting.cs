using System.Globalization;
using Autodesk.Revit.DB;
using Nice3point.Revit.Extensions;
using RevitModelMcp.Capture;
using RevitModelMcp.Core.Control;
using RevitModelMcp.Core.Fork;

namespace RevitModelMcp.Control.Fork;

/// <summary>
/// Reads and applies one view's lighting state: shadows, sun position, ground plane, display background and the
/// rendering lighting scheme. The sun and shadow settings belong to the view, so a locked or shared element is
/// reported rather than silently changed for other views too. Runs inside the transaction the action executor
/// already opened, so a dry run is rolled back by the executor, not here.
/// </summary>
internal static class ForkLighting
{
    /// <summary>Gradient used when a caller asks for a gradient without colors of its own.</summary>
    private static readonly string[] DefaultGradientColors = ["#C8DEF0", "#F5F5F5", "#BFBFBF"];

    private const string Command = "set-view-lighting";

    internal static View Resolve(Document document, string? reference)
    {
        if (string.IsNullOrWhiteSpace(reference))
        {
            throw new ArgumentException("view is required.");
        }

        var view = ReadCommandReader.FindView(document, reference!.Trim())
            ?? throw new ArgumentException($"View '{reference}' was not found.");
        if (view.IsTemplate)
        {
            throw new ArgumentException($"View '{view.Name}' is a template; lighting is set on a non-template view.");
        }

        return view;
    }

    /// <summary>Resolves the addressed view and refuses one that carries no sun and shadow settings at all.</summary>
    internal static View ResolveForLighting(Document document, string? reference)
    {
        var view = Resolve(document, reference);
        if (ReadSunSettings(view) is null)
        {
            throw new ArgumentException(
                $"View '{view.Name}' is a {view.ViewType} view and has no sun and shadow settings to change.");
        }

        return view;
    }

    /// <summary>Rejects an input the wire contract cannot judge: one change at least, and paired sun angles.</summary>
    internal static void Validate(ActionJobContract action)
    {
        Require(action.Options.Shadows.HasValue || action.Options.ShadowIntensity.HasValue || action.Options.SunlightIntensity.HasValue
                || action.Options.SunDate is not null || action.Options.SunTime is not null
                || action.Options.SunAzimuthDeg.HasValue || action.Options.SunAltitudeDeg.HasValue
                || action.Options.GroundPlane.HasValue || action.Options.GroundPlaneLevel is not null
                || action.Options.Background is not null || action.Options.LightingScheme is not null,
            "Provide at least one lighting setting to change.");
        Require(action.Options.ShadowIntensity is null or (>= 0 and <= 100), "shadowIntensity must be between 0 and 100.");
        Require(action.Options.SunlightIntensity is null or (>= 0 and <= 100), "sunlightIntensity must be between 0 and 100.");
        if (action.Options.SunDate is not null)
        {
            Require(DateTime.TryParseExact(action.Options.SunDate.Trim(), "yyyy-MM-dd", CultureInfo.InvariantCulture,
                DateTimeStyles.None, out _), "sunDate must use yyyy-MM-dd.");
        }

        if (action.Options.SunTime is not null)
        {
            Require(DateTime.TryParseExact(action.Options.SunTime.Trim(), "HH:mm", CultureInfo.InvariantCulture,
                DateTimeStyles.None, out _), "sunTime must use 24-hour HH:mm.");
        }

        Require(action.Options.SunAzimuthDeg.HasValue == action.Options.SunAltitudeDeg.HasValue,
            "sunAzimuthDeg and sunAltitudeDeg must be provided together.");
        Require(action.Options.SunAzimuthDeg is null or (>= 0 and <= 360), "sunAzimuthDeg must be between 0 and 360.");
        Require(action.Options.SunAltitudeDeg is null or (>= -90 and <= 90), "sunAltitudeDeg must be between -90 and 90.");
        if (action.Options.Background is not null)
        {
            Require(action.Options.Background.Trim().ToLowerInvariant() is "sky" or "gradient", "background must be 'sky' or 'gradient'.");
        }

        if (action.Options.BackgroundColors is not null)
        {
            Require(action.Options.Background?.Trim().ToLowerInvariant() == "gradient", "backgroundColors requires background 'gradient'.");
            Require(action.Options.BackgroundColors.Count == 3 && action.Options.BackgroundColors.All(IsHexColor),
                "backgroundColors must hold three '#RRGGBB' colors: sky, horizon, ground.");
        }

        if (action.Options.LightingScheme is not null)
        {
            Require(action.Options.LightingScheme.Trim().ToLowerInvariant() is "exterior-sun" or "exterior-sun-and-artificial"
                    or "exterior-artificial" or "interior-sun" or "interior-sun-and-artificial" or "interior-artificial",
                "lightingScheme must be exterior-sun, exterior-sun-and-artificial, exterior-artificial, interior-sun, interior-sun-and-artificial or interior-artificial.");
        }
    }

    internal static ViewLightingFacts Read(Document document, View view)
    {
        var facts = new ViewLightingFacts
        {
            ViewId = RevitValueReader.GetId(view.Id),
            View = view.Name,
            ViewType = view.ViewType.ToString()
        };
        ReadIfAvailable(() => facts.ShadowIntensity = view.ShadowIntensity);
        ReadIfAvailable(() => facts.SunlightIntensity = view.SunlightIntensity);
        var settings = ReadSunSettings(view);
        if (settings is not null)
        {
            var type = settings.SunAndShadowType;
            facts.SunType = type.ToString();
            facts.SunSettingsShared = settings.SharesSettings;
            ReadIfAvailable(() => facts.Shadows = settings.Visible);
            ReadIfAvailable(() =>
            {
                facts.SunDateAndTimeUtc = settings.StartDateAndTime.ToUniversalTime()
                    .ToString("yyyy-MM-dd'T'HH:mm:ss'Z'", CultureInfo.InvariantCulture);
                facts.SunTimeZoneHours = Math.Round(settings.TimeZone, 2);
                facts.SunUsesDst = settings.UsesDST;
            });
            if (type == SunAndShadowType.Lighting)
            {
                ReadIfAvailable(() => facts.SunAzimuthDeg = Math.Round(RadiansToDegrees(settings.Azimuth), 1));
                ReadIfAvailable(() => facts.SunAltitudeDeg = Math.Round(RadiansToDegrees(settings.Altitude), 1));
            }

            ReadIfAvailable(() => facts.GroundPlane = settings.UsesGroundPlane);
            ReadIfAvailable(() => facts.GroundPlaneLevel = settings.GroundPlaneLevelId.ToElement<Level>(document)?.Name);
        }

        ReadIfAvailable(() =>
        {
            using var background = view.GetBackground();
            if (background is null)
            {
                return;
            }

            facts.Background = background.Type.ToString();
            if (background.Type == ViewDisplayBackgroundType.Gradient)
            {
                facts.BackgroundColors =
                [
                    Hex(background.SkyColor),
                    Hex(background.BackgroundColor),
                    Hex(background.GroundColor)
                ];
            }
        });
        if (view is View3D threeDimensional)
        {
            ReadIfAvailable(() =>
            {
                using var rendering = threeDimensional.GetRenderingSettings();
                facts.LightingScheme = SchemeName(rendering.LightingSource);
            });
        }

        return facts;
    }

    /// <summary>Applies the requested lighting settings inside the caller's transaction.</summary>
    internal static ActionResultData Apply(Document document, ActionJobContract action)
    {
        Validate(action);
        var view = ResolveForLighting(document, action.View);
        var settings = ReadSunSettings(view)!;
        var notes = new List<string>();
        var changes = 0;
        var sunChanged = false;
        if (action.Options.Shadows.HasValue)
        {
            SetShadows(settings, action.Options.Shadows.Value);
            changes++;
        }

        if (action.Options.ShadowIntensity.HasValue)
        {
            view.ShadowIntensity = action.Options.ShadowIntensity.Value;
            changes++;
        }

        if (action.Options.SunlightIntensity.HasValue)
        {
            view.SunlightIntensity = action.Options.SunlightIntensity.Value;
            changes++;
        }

        if (action.Options.SunDate is not null || action.Options.SunTime is not null)
        {
            ApplySunDateAndTime(settings, action);
            sunChanged = true;
            changes++;
        }

        if (action.Options.SunAzimuthDeg.HasValue)
        {
            // A fixed sun position is the lighting study type: date and time no longer drive the sun.
            settings.SunAndShadowType = SunAndShadowType.Lighting;
            settings.Azimuth = DegreesToRadians(action.Options.SunAzimuthDeg.Value);
            settings.Altitude = DegreesToRadians(action.Options.SunAltitudeDeg!.Value);
            sunChanged = true;
            changes++;
        }

        if (action.Options.GroundPlane.HasValue)
        {
            settings.UsesGroundPlane = action.Options.GroundPlane.Value;
            sunChanged = true;
            changes++;
        }

        if (action.Options.GroundPlaneLevel is not null)
        {
            SetGroundPlaneLevel(settings, ResolveLevel(document, action.Options.GroundPlaneLevel), notes);
            sunChanged = true;
            changes++;
        }

        if (action.Options.Background is not null)
        {
            ApplyBackground(view, action);
            changes++;
        }

        if (action.Options.LightingScheme is not null)
        {
            ApplyLightingScheme(view, action.Options.LightingScheme);
            changes++;
        }

        if (sunChanged && settings.SharesSettings)
        {
            notes.Add("This view shares its sun and shadow settings, so the change reaches every view that shares them.");
        }

        return new ActionResultData
        {
            ViewId = RevitValueReader.GetId(view.Id),
            ViewName = view.Name,
            Count = changes,
            Notes = notes.Count > 0 ? notes : null
        };
    }

    private static void ApplySunDateAndTime(SunAndShadowSettings settings, ActionJobContract action)
    {
        var local = ProjectLocalTime(settings);
        var date = action.Options.SunDate is null
            ? local.Date
            : DateTime.ParseExact(action.Options.SunDate.Trim(), "yyyy-MM-dd", CultureInfo.InvariantCulture).Date;
        var time = action.Options.SunTime is null
            ? local.TimeOfDay
            : TimeSpan.ParseExact(action.Options.SunTime.Trim(), @"hh\:mm", CultureInfo.InvariantCulture);
        // Revit reads a still image from one point in time, so a study type that spans a range is switched first.
        settings.SunAndShadowType = SunAndShadowType.StillImage;
        var requested = date.Add(time);
        settings.StartDateAndTime = DateTime.SpecifyKind(requested, DateTimeKind.Local);
    }

    /// <summary>
    /// Reads the current sun date and time back in the project time zone the settings carry, so a caller that
    /// passes only a date or only a time keeps the other half of what the view already shows.
    /// </summary>
    private static DateTime ProjectLocalTime(SunAndShadowSettings settings)
    {
        var utc = settings.StartDateAndTime.ToUniversalTime();
        return utc.AddHours(settings.TimeZone);
    }

    /// <summary>
    /// Switches the view's shadows through the per-view sun and shadow settings. Revit exposes no parameter for
    /// the Graphic Display Options "Shadows" checkbox: the per-view element's Visible is the switch the API
    /// offers, and a settings element shared between views cannot carry a per-view switch at all.
    /// </summary>
    private static void SetShadows(SunAndShadowSettings settings, bool value)
    {
        if (settings.SharesSettings)
        {
            throw new ArgumentException(
                "This view shares its sun and shadow settings, so Revit cannot switch shadows for this view alone.");
        }

        settings.Visible = value;
    }

    private static void SetGroundPlaneLevel(SunAndShadowSettings settings, Level level, List<string> notes)
    {
        try
        {
            settings.GroundPlaneLevelId = level.Id;
        }
        catch (Autodesk.Revit.Exceptions.ArgumentException)
        {
            // Revit only accepts a level it knows as a ground plane, so mark the requested one and try again.
            var isGroundPlane = level.get_Parameter(BuiltInParameter.LEVEL_IS_GROUND_PLANE)
                ?? throw new ArgumentException(
                    $"Level '{level.Name}' cannot be a ground plane: Revit exposes no ground plane setting on it.");
            if (isGroundPlane.IsReadOnly)
            {
                throw new ArgumentException(
                    $"Level '{level.Name}' is not a ground plane and its ground plane flag is read-only.");
            }

            isGroundPlane.Set(1);
            settings.GroundPlaneLevelId = level.Id;
            notes.Add($"Level '{level.Name}' was marked as a ground plane because Revit only accepts a ground plane level.");
        }

        if (!settings.UsesGroundPlane)
        {
            settings.UsesGroundPlane = true;
            notes.Add("The ground plane was switched on because a ground plane level was requested.");
        }
    }

    private static Level ResolveLevel(Document document, string name)
    {
        var levels = new FilteredElementCollector(document).OfClass(typeof(Level)).Cast<Level>()
            .Where(level => level.Name.Length > 0).ToList();
        var level = levels.FirstOrDefault(candidate => string.Equals(candidate.Name, name, StringComparison.Ordinal))
                    ?? levels.FirstOrDefault(candidate => string.Equals(candidate.Name, name, StringComparison.OrdinalIgnoreCase));
        if (level is not null)
        {
            return level;
        }

        var closest = ActionJobParser.ClosestFamilyNames(name, levels.Select(candidate => candidate.Name));
        throw new ArgumentException(closest.Count == 0
            ? $"Level '{name}' was not found."
            : $"Level '{name}' was not found. Close names: {string.Join(", ", closest)}.");
    }

    private static void ApplyBackground(View view, ActionJobContract action)
    {
        try
        {
            if (action.Options.Background!.Trim().ToLowerInvariant() == "sky")
            {
                view.SetBackground(ViewDisplayBackground.CreateSky());
                return;
            }

            var colors = action.Options.BackgroundColors ?? CurrentGradientColors(view);
            view.SetBackground(ViewDisplayBackground.CreateGradient(
                ParseColor(colors[0]), ParseColor(colors[1]), ParseColor(colors[2])));
        }
        catch (Autodesk.Revit.Exceptions.ArgumentException exception)
        {
            throw new ArgumentException($"View '{view.Name}' cannot take that background: {exception.Message}");
        }
    }

    private static List<string> CurrentGradientColors(View view)
    {
        using var background = view.GetBackground();
        return background is not null && background.Type == ViewDisplayBackgroundType.Gradient
            ? [Hex(background.SkyColor), Hex(background.BackgroundColor), Hex(background.GroundColor)]
            : [.. DefaultGradientColors];
    }

    private static void ApplyLightingScheme(View view, string scheme)
    {
        if (view is not View3D threeDimensional)
        {
            throw new ArgumentException(
                $"The rendering lighting scheme is only available on a 3D view, and '{view.Name}' is a {view.ViewType} view.");
        }

        using var rendering = threeDimensional.GetRenderingSettings();
        rendering.LightingSource = scheme.Trim().ToLowerInvariant() switch
        {
            "exterior-sun" => LightingSource.ExteriorSun,
            "exterior-sun-and-artificial" => LightingSource.ExteriorSunAndArtificial,
            "exterior-artificial" => LightingSource.ExteriorArtificial,
            "interior-sun" => LightingSource.InteriorSun,
            "interior-sun-and-artificial" => LightingSource.InteriorSunAndArtificial,
            "interior-artificial" => LightingSource.InteriorArtificial,
            _ => throw new ArgumentException($"Unknown lighting scheme '{scheme}'.")
        };
        threeDimensional.SetRenderingSettings(rendering);
    }

    private static string SchemeName(LightingSource source) => source switch
    {
        LightingSource.ExteriorSun => "exterior-sun",
        LightingSource.ExteriorSunAndArtificial => "exterior-sun-and-artificial",
        LightingSource.ExteriorArtificial => "exterior-artificial",
        LightingSource.InteriorSun => "interior-sun",
        LightingSource.InteriorSunAndArtificial => "interior-sun-and-artificial",
        LightingSource.InteriorArtificial => "interior-artificial",
        _ => source.ToString()
    };

    private static Color ParseColor(string value)
    {
        if (value is not { Length: 7 } || value[0] != '#'
            || !byte.TryParse(value.Substring(1, 2), NumberStyles.HexNumber, CultureInfo.InvariantCulture, out var red)
            || !byte.TryParse(value.Substring(3, 2), NumberStyles.HexNumber, CultureInfo.InvariantCulture, out var green)
            || !byte.TryParse(value.Substring(5, 2), NumberStyles.HexNumber, CultureInfo.InvariantCulture, out var blue))
        {
            throw new ArgumentException($"'{value}' is not a '#RRGGBB' color.");
        }

        return new Color(red, green, blue);
    }

    private static bool IsHexColor(string value) =>
        value.Length == 7 && value[0] == '#' && value[1..].All(char.IsAsciiHexDigit);

    private static string Hex(Color color) =>
        $"#{color.Red:X2}{color.Green:X2}{color.Blue:X2}";

    private static SunAndShadowSettings? ReadSunSettings(View view)
    {
        SunAndShadowSettings? settings = null;
        ReadIfAvailable(() => settings = view.SunAndShadowSettings);
        return settings;
    }

    /// <summary>
    /// Reads a setting that only some views expose. A reading that Revit refuses stays null in the facts rather
    /// than failing the action, which is what lets one response describe any view.
    /// </summary>
    private static void ReadIfAvailable(Action read)
    {
        try
        {
            read();
        }
        catch (Autodesk.Revit.Exceptions.InvalidOperationException)
        {
        }
        catch (Autodesk.Revit.Exceptions.ArgumentException)
        {
        }
    }

    private static void Require(bool condition, string message)
    {
        if (!condition)
        {
            throw new ArgumentException(message);
        }
    }

    private static double DegreesToRadians(double degrees) => degrees * Math.PI / 180.0;

    private static double RadiansToDegrees(double radians) => radians * 180.0 / Math.PI;
}
