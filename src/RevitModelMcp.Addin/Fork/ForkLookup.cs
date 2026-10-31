using System.Globalization;
using Autodesk.Revit.DB;
using Nice3point.Revit.Extensions;
using RevitModelMcp.Capture;

namespace RevitModelMcp.Control.Fork;

/// <summary>
/// Lookups every fork action needs: a level, a phase and a family type by exact name, plus unit conversion.
/// Upstream keeps its own private copies of these; the fork cannot reach them, so it keeps one set here
/// instead of repeating the collector dance in each action file.
/// </summary>
internal static class ForkLookup
{
    /// <summary>Resolves a level by its exact name, or null when the document holds none.</summary>
    internal static Level? LevelOrNull(Document document, string name)
    {
        using var levels = document.CollectElements().OfClass<Level>()
            .WhereParameter(BuiltInParameter.DATUM_TEXT).Equals(name);
        return levels.FirstOrDefault() as Level;
    }

    /// <summary>Resolves a level by its exact name.</summary>
    internal static Level Level(Document document, string name) =>
        LevelOrNull(document, name) ?? throw new ArgumentException($"Level '{name}' was not found.");

    /// <summary>Resolves a phase by name, ignoring case, as the Revit UI does.</summary>
    internal static Phase Phase(Document document, string name)
    {
        using var phases = document.CollectElements().OfClass<Phase>();
        return phases.Cast<Phase>()
                   .FirstOrDefault(phase => string.Equals(phase.Name, name, StringComparison.OrdinalIgnoreCase))
               ?? throw new ArgumentException(
                   $"Phase '{name}' was not found. Use revit_list_catalog(section=\"phases\") for exact names.");
    }

    /// <summary>Name of a phase, or an empty string for none.</summary>
    internal static string PhaseName(Document document, ElementId phaseId)
    {
        if (phaseId is null || phaseId == ElementId.InvalidElementId) return string.Empty;
        return phaseId.ToElement<Phase>(document)?.Name ?? string.Empty;
    }

    /// <summary>Millimetres to Revit's internal feet.</summary>
    internal static double Millimeters(double value) => UnitUtils.ConvertToInternalUnits(value, UnitTypeId.Millimeters);

    /// <summary>Revit's internal feet to millimetres, rounded to one decimal for reporting.</summary>
    internal static double MillimetersFromInternal(double value) => Math.Round(RevitValueReader.ToMillimeters(value), 1);

    /// <summary>Throws the documented argument error when a check fails.</summary>
    internal static void Require(bool condition, string message)
    {
        if (!condition) throw new ArgumentException(message);
    }

    /// <summary>Element id of a wire value, as the add-in's own id factory builds it.</summary>
    internal static ElementId CreateId(long value) => ActionCommandExecutor.CreateId(value);

    /// <summary>Formats a number the way the fork's messages and readings do.</summary>
    internal static string Number(double value) => value.ToString("R", CultureInfo.InvariantCulture);
}
