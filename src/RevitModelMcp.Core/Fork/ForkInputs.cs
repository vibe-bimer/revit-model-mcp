using System.Globalization;
using RevitModelMcp.Core.Control;

namespace RevitModelMcp.Core.Fork;

/// <summary>
/// Reads the fork's action inputs out of the job's single <c>fork</c> bag. Upstream carries that one
/// generic member for the fork, so a fork action adds inputs without editing an upstream field list; each
/// command declares the keys it accepts and an unknown key is refused instead of quietly ignored. The
/// values land on the fork's own tail of the action contract, which is where the fork actions read them.
/// See adr/0005.
/// </summary>
public static class ForkInputs
{
    /// <summary>Keys each fork command reads, with the contract field each one fills.</summary>
    private static readonly Dictionary<string, Dictionary<string, Action<ActionJobContract, object?>>> Commands =
        new(StringComparer.Ordinal)
        {
            ["set-view-lighting"] = new(StringComparer.Ordinal)
            {
                ["shadows"] = (action, value) => action.Shadows = Flag("shadows", value),
                ["shadowIntensity"] = (action, value) => action.ShadowIntensity = Whole("shadowIntensity", value),
                ["sunlightIntensity"] = (action, value) => action.SunlightIntensity = Whole("sunlightIntensity", value),
                ["sunDate"] = (action, value) => action.SunDate = Text("sunDate", value),
                ["sunTime"] = (action, value) => action.SunTime = Text("sunTime", value),
                ["sunAzimuthDeg"] = (action, value) => action.SunAzimuthDeg = Number("sunAzimuthDeg", value),
                ["sunAltitudeDeg"] = (action, value) => action.SunAltitudeDeg = Number("sunAltitudeDeg", value),
                ["groundPlane"] = (action, value) => action.GroundPlane = Flag("groundPlane", value),
                ["groundPlaneLevel"] = (action, value) => action.GroundPlaneLevel = Text("groundPlaneLevel", value),
                ["background"] = (action, value) => action.Background = Text("background", value),
                ["backgroundColors"] = (action, value) => action.BackgroundColors = Texts("backgroundColors", value),
                ["lightingScheme"] = (action, value) => action.LightingScheme = Text("lightingScheme", value)
            }
        };

    /// <summary>Copies the bag onto the action's fork inputs and refuses a key the command does not accept.</summary>
    public static void Read(ActionJobContract action, string command, Dictionary<string, object>? bag)
    {
        if (action is null) throw new ArgumentNullException(nameof(action));
        if (bag is null || bag.Count == 0) return;
        if (!Commands.TryGetValue(command, out var inputs))
            throw new ArgumentException($"{command} accepts no fork inputs.");
        foreach (var (key, value) in bag)
        {
            if (!inputs.TryGetValue(key, out var set))
                throw new ArgumentException($"{command} does not accept fork.{key}.");
            set(action, value);
        }
    }

    /// <summary>Whether the command reads fork inputs at all.</summary>
    public static bool Accepts(string command) => Commands.ContainsKey(command);

    private static bool? Flag(string key, object? value) => value switch
    {
        null => null,
        bool flag => flag,
        string text when bool.TryParse(text.Trim(), out var parsed) => parsed,
        int number => number != 0,
        long number => number != 0,
        decimal number => number != 0,
        double number => number != 0,
        _ => throw Invalid(key, "true or false")
    };

    private static int? Whole(string key, object? value) => value switch
    {
        null => null,
        int number => number,
        long number => number is >= int.MinValue and <= int.MaxValue
            ? (int)number
            : throw Invalid(key, "a whole number in range"),
        decimal number when number == Math.Floor(number) && number is >= int.MinValue and <= int.MaxValue => (int)number,
        double number when number == Math.Floor(number) && number is >= int.MinValue and <= int.MaxValue => (int)number,
        string text when int.TryParse(text.Trim(), NumberStyles.Integer, CultureInfo.InvariantCulture, out var parsed) => parsed,
        _ => throw Invalid(key, "a whole number")
    };

    private static double? Number(string key, object? value) => value switch
    {
        null => null,
        int number => number,
        long number => number,
        decimal number => (double)number,
        double number => number,
        string text when double.TryParse(text.Trim(), NumberStyles.Float, CultureInfo.InvariantCulture, out var parsed) => parsed,
        _ => throw Invalid(key, "a number")
    };

    private static string? Text(string key, object? value) => value switch
    {
        null => null,
        string text => text,
        _ => throw Invalid(key, "text")
    };

    private static List<string>? Texts(string key, object? value) => value switch
    {
        null => null,
        object?[] items => Items(key, items),
        List<object?> items => Items(key, items),
        _ => throw Invalid(key, "a list of three '#RRGGBB' colors")
    };

    private static List<string> Items(string key, IReadOnlyList<object?> values) =>
        values.Select(item => item as string ?? throw Invalid(key, "a list of three '#RRGGBB' colors")).ToList();

    private static ArgumentException Invalid(string key, string expected) => new($"fork.{key} must be {expected}.");
}
