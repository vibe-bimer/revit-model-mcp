using System.IO;
using Autodesk.Revit.DB;
using Nice3point.Revit.Extensions;
using RevitModelMcp.Capture;
using RevitModelMcp.Core.Control;
using RevitModelMcp.Core.Fork;

namespace RevitModelMcp.Control.Fork;

/// <summary>
/// Loads one family file from the workstation: the whole family, or a single type when one is named.
/// The load always carries an <see cref="IFamilyLoadOptions"/>, because Revit answers a load without one
/// through its own dialog — which blocks an unattended run forever. The default answers continue the load
/// without overwriting the parameter values the project already holds, and an existing family is reused
/// rather than replaced. See docs/modeling-tools.md.
/// </summary>
internal static class ForkFamilies
{
    /// <summary>Checks the family path before anything is loaded.</summary>
    internal static void Validate(ActionJobContract action)
    {
        var path = action.Options.FamilyPath;
        ForkLookup.Require(!string.IsNullOrWhiteSpace(path), "path is required.");
        // The same absolute-path rule every upstream file action follows: no cloud paths, no traversal.
        DocumentPathValidator.Validate(path, "path");
        ForkLookup.Require(File.Exists(path), MissingMessage(path!));
    }

    /// <summary>Loads the family and reports whether it was new, with every type it now offers.</summary>
    internal static ActionResultData Apply(Document document, ActionJobContract action)
    {
        Validate(action);
        var path = action.Options.FamilyPath!;
        var typeName = action.Options.FamilyTypeName?.Trim();
        var overwrite = action.Options.OverwriteParameters ?? false;
        var familyName = Path.GetFileNameWithoutExtension(path);
        var existing = FamilyOrNull(document, familyName);

        // A family that is already in the project is reused rather than reloaded: Revit refuses a second
        // load of the same file, and the caller asked for the family, not for a refresh of it.
        if (existing is not null && !overwrite)
        {
            if (!string.IsNullOrEmpty(typeName) && SymbolOrNull(existing, typeName) is null)
                throw new ArgumentException(TypeMessage(document, familyName, typeName, path));
            return Loaded(document, existing, "existing");
        }

        Family family;
        if (string.IsNullOrEmpty(typeName))
        {
            var options = new ForkFamilyLoadOptions(overwrite);
            if (!document.LoadFamily(path, options, out family))
                throw new ArgumentException($"Could not load family '{familyName}' from '{path}'.");
        }
        else
        {
            var options = new ForkFamilyLoadOptions(overwrite);
            if (!document.LoadFamilySymbol(path, typeName, options, out var symbol))
                throw new ArgumentException(TypeMessage(document, familyName, typeName, path));
            family = symbol.Family;
        }

        return Loaded(document, family, existing is null ? "new" : "existing");
    }

    private static ActionResultData Loaded(Document document, Family family, string state) => new()
    {
        Id = RevitValueReader.GetId(family.Id),
        Category = family.Category?.Name,
        ForkOutcome = new ForkOutcome
        {
            State = state,
            FamilyName = family.Name,
            FamilyTypes = Types(document, family)
        }
    };

    /// <summary>Reads the family a load reported as an element fact block.</summary>
    internal static ActionFacts Read(Document document, ElementId id, string? typeName)
    {
        if (id.ToElement(document) is not { } element) return new ActionFacts();
        return new ActionFacts
        {
            Id = RevitValueReader.GetId(element.Id),
            Category = element.Category?.Name,
            Family = element.Name,
            Type = typeName
        };
    }

    private static string TypeMessage(Document document, string familyName, string typeName, string path)
    {
        var loaded = FamilyOrNull(document, familyName);
        if (loaded is null) return $"Could not load type '{typeName}' from '{path}'.";
        var names = Types(document, loaded).Select(type => type.Name).ToList();
        var available = names.Count == 0 ? "none" : string.Join(", ", names);
        return $"Type '{typeName}' is not in family '{familyName}'. Available types: {available}.";
    }

    private static List<ForkFamilyType> Types(Document document, Family family)
    {
        var types = new List<ForkFamilyType>();
        foreach (var id in family.GetFamilySymbolIds())
        {
            if (document.GetElement(id) is not FamilySymbol symbol) continue;
            types.Add(new ForkFamilyType { Id = RevitValueReader.GetId(symbol.Id), Name = symbol.Name });
        }

        types.Sort((left, right) => string.CompareOrdinal(left.Name, right.Name));
        return types;
    }

    private static Family? FamilyOrNull(Document document, string name)
    {
        using var families = document.CollectElements().OfClass<Family>();
        return families.Cast<Family>()
            .FirstOrDefault(family => string.Equals(family.Name, name, StringComparison.OrdinalIgnoreCase));
    }

    private static FamilySymbol? SymbolOrNull(Family family, string typeName) => family.GetFamilySymbolIds()
        .Select(id => family.Document.GetElement(id))
        .OfType<FamilySymbol>()
        .FirstOrDefault(symbol => string.Equals(symbol.Name, typeName, StringComparison.OrdinalIgnoreCase));

    private static string MissingMessage(string path)
    {
        var directory = Path.GetDirectoryName(path);
        var closest = Closest(directory, Path.GetFileName(path));
        var hint = closest.Count == 0 ? string.Empty : $" Closest: {string.Join(", ", closest)}.";
        return $"Family file '{path}' was not found.{hint}";
    }

    /// <summary>
    /// Names the family files the caller most likely meant. A typo usually keeps most of the name, so the
    /// ranking is by edit distance and the caller is shown three at most.
    /// </summary>
    private static List<string> Closest(string? directory, string fileName)
    {
        if (string.IsNullOrEmpty(directory) || !Directory.Exists(directory)) return [];
        var candidates = Directory.EnumerateFiles(directory, "*.rfa")
            .Select(Path.GetFileName)
            .Where(name => !string.IsNullOrEmpty(name))
            .Select(name => (Name: name!, Distance: Distance(name!, fileName)))
            .OrderBy(candidate => candidate.Distance)
            .ThenBy(candidate => candidate.Name, StringComparer.OrdinalIgnoreCase)
            .Take(3)
            .Select(candidate => candidate.Name)
            .ToList();
        return candidates;
    }

    private static int Distance(string left, string right)
    {
        var previous = new int[right.Length + 1];
        var current = new int[right.Length + 1];
        for (var column = 0; column <= right.Length; column++) previous[column] = column;
        for (var row = 1; row <= left.Length; row++)
        {
            current[0] = row;
            for (var column = 1; column <= right.Length; column++)
            {
                var cost = char.ToUpperInvariant(left[row - 1]) == char.ToUpperInvariant(right[column - 1]) ? 0 : 1;
                current[column] = Math.Min(
                    Math.Min(current[column - 1] + 1, previous[column] + 1),
                    previous[column - 1] + cost);
            }

            (previous, current) = (current, previous);
        }

        return previous[right.Length];
    }

    /// <summary>
    /// The load options every family load must carry. Revit asks these two questions only when the family is
    /// both loaded and changed; answering them here is what keeps the load off its own dialog.
    /// </summary>
    private sealed class ForkFamilyLoadOptions(bool overwriteParameters) : IFamilyLoadOptions
    {
        /// <summary>Continues the load, and leaves the project's parameter values alone unless asked.</summary>
        public bool OnFamilyFound(bool familyInUse, out bool overwriteParameterValues)
        {
            overwriteParameterValues = overwriteParameters;
            return true;
        }

        /// <summary>Continues a shared family load from the project, with the same overwrite answer.</summary>
        public bool OnSharedFamilyFound(
            Family sharedFamily,
            bool familyInUse,
            out FamilySource source,
            out bool overwriteParameterValues)
        {
            source = FamilySource.Project;
            overwriteParameterValues = overwriteParameters;
            return true;
        }
    }
}
