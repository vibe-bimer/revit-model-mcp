using System.Globalization;
using System.IO;
using Autodesk.Revit.DB;
using RevitModelMcp.Core.Control;
using RevitModelMcp.Core.Models;
using RevitModelMcp.Output;

namespace RevitModelMcp.Capture;

/// <summary>
/// Writes the element identifier list of the drawn components to a workbook on this workstation.
/// The list is ordered by the classification hierarchy so it can be read as a component register;
/// the identifier itself stays read-only, because the Revit API cannot assign an <see cref="ElementId"/>.
/// </summary>
internal static class ElementIdExportReader
{
    private const string SheetName = "构件ID清单";
    private const string ExportFolder = "Exports";
    private const int MaxRows = 50_000;

    private static readonly string[] DefaultFields =
    {
        "category", "family", "type", "level", "id", "name", "workset"
    };

    /// <summary>Sort keys in priority order; only the ones present in the field list are used.</summary>
    private static readonly string[] SortFields = { "category", "family", "type" };

    private static readonly Dictionary<string, string> HeaderLabels = new(StringComparer.OrdinalIgnoreCase)
    {
        ["category"] = "类别",
        ["family"] = "族",
        ["type"] = "类型",
        ["level"] = "标高",
        ["id"] = "构件ID",
        ["name"] = "名称",
        ["workset"] = "工作集",
        ["phase"] = "阶段",
        ["areaScheme"] = "面积方案",
        ["hasWarnings"] = "有警告"
    };

    private static readonly int[] ColumnWidths = { 16, 22, 26, 14, 12, 26, 16, 14, 16, 12 };

    /// <summary>
    /// Model categories that hold datums, materials or view infrastructure rather than drawn
    /// components. Annotation and view categories never reach this list: they are excluded by
    /// <see cref="CategoryType.Model"/>, view-specific elements and element types.
    /// </summary>
    /// <summary>Enum-name fragments that mark a category as infrastructure rather than a component.</summary>
    private static readonly string[] ExcludedNameFragments = { "CenterLine", "Centerline", "Asset", "SunPath" };

    private static readonly HashSet<BuiltInCategory> ExcludedCategories = new()
    {
        BuiltInCategory.OST_Levels,
        BuiltInCategory.OST_Grids,
        BuiltInCategory.OST_CLines,
        BuiltInCategory.OST_CenterLines,
        BuiltInCategory.OST_Lines,
        BuiltInCategory.OST_Materials,
        BuiltInCategory.OST_AppearanceAsset,
        BuiltInCategory.OST_PropertySet,
        BuiltInCategory.OST_SunStudy,
        BuiltInCategory.OST_Cameras,
        BuiltInCategory.OST_SectionBox,
        BuiltInCategory.OST_ProjectBasePoint,
        BuiltInCategory.OST_SharedBasePoint,
        BuiltInCategory.OST_Views,
        BuiltInCategory.OST_Sheets,
        BuiltInCategory.OST_TitleBlocks,
        BuiltInCategory.OST_Viewports,
        BuiltInCategory.OST_Schedules,
        BuiltInCategory.OST_LegendComponents,
        BuiltInCategory.OST_PreviewLegendComponents,
        BuiltInCategory.OST_ProjectInformation,
        BuiltInCategory.OST_PipingSystem,
        BuiltInCategory.OST_DuctSystem,
        BuiltInCategory.OST_HVAC_Zones,
        BuiltInCategory.OST_SunPath1,
        BuiltInCategory.OST_SunPath2,
        BuiltInCategory.OST_AnalysisDisplayStyle,
        BuiltInCategory.OST_TopographyContours,
        BuiltInCategory.OST_SecondaryTopographyContours
    };

    internal static ElementIdExportData Read(Document document, ControlJobParseResult job)
    {
        var fields = job.Fields.Count > 0 ? job.Fields.ToList() : DefaultFields.ToList();
        var headers = fields.Select(Header).ToList();
        var fieldReader = new ElementFieldReader(document);

        var rows = new List<PreparedQueryRecord>();
        var skipped = new Dictionary<(string Name, string BuiltIn), int>();
        var builtInByCategory = new Dictionary<string, string>(StringComparer.Ordinal);
        var total = 0;
        foreach (var element in new FilteredElementCollector(document).WhereElementIsNotElementType())
        {
            if (!IsDrawnComponent(element))
            {
                // Keep the rejected categories visible so the rule can be checked and corrected.
                var name = element.Category?.Name;
                if (!string.IsNullOrEmpty(name))
                {
                    var key = (name, BuiltInName(element));
                    skipped[key] = skipped.TryGetValue(key, out var count) ? count + 1 : 1;
                }

                continue;
            }

            total++;
            if (element.Category is { } included)
            {
                builtInByCategory[included.Name] = BuiltInName(element);
            }

            if (rows.Count >= MaxRows)
            {
                continue;
            }

            rows.Add(fieldReader.Prepare(element, fields));
        }

        Sort(rows, fields);

        var path = ResolvePath(document, job.SaveTo);
        var sheet = new XlsxSheet(SheetName, headers, ColumnWidths);
        foreach (var record in rows)
        {
            sheet.AddRow(fields.Select(field => Cell(record, field)).ToList());
        }

        sheet.Save(path);

        return new ElementIdExportData
        {
            Path = path,
            FileName = Path.GetFileName(path),
            SheetName = SheetName,
            Columns = headers,
            RowCount = rows.Count,
            TotalCandidates = total,
            Truncated = total > rows.Count,
            SizeBytes = new FileInfo(path).Length,
            CategoryCounts = CountCategories(rows, fields, builtInByCategory),
            SkippedCategories = skipped
                .Select(entry => new ElementCategoryCount
                {
                    Category = entry.Key.Name,
                    BuiltInCategory = entry.Key.BuiltIn,
                    Count = entry.Value
                })
                .OrderByDescending(entry => entry.Count)
                .ThenBy(entry => entry.Category, StringComparer.Ordinal)
                .Take(20)
                .ToList()
        };
    }

    private static bool IsDrawnComponent(Element element)
    {
        // Datums and model text are never drawn components: the reference plane category has no
        // BuiltInCategory member of its own, and model text shares the generic model category.
        if (element is Level or Grid or ReferencePlane or ModelText || element.ViewSpecific)
        {
            return false;
        }

        var category = element.Category;
        if (category is null || category.CategoryType != CategoryType.Model)
        {
            return false;
        }

        var builtIn = (BuiltInCategory)RevitValueReader.GetId(category.Id);
        if (ExcludedCategories.Contains(builtIn))
        {
            return false;
        }

        // MEP centre lines, appearance assets and sun paths come as families of categories whose
        // localized names differ per language; the enum name stays stable, so match on that.
        var name = builtIn.ToString();
        return !ExcludedNameFragments.Any(fragment => name.Contains(fragment, StringComparison.Ordinal));
    }

    private static string BuiltInName(Element element)
    {
        var category = element.Category;
        return category is null
            ? string.Empty
            : ((BuiltInCategory)RevitValueReader.GetId(category.Id)).ToString();
    }

    private static void Sort(List<PreparedQueryRecord> rows, IReadOnlyList<string> fields)
    {
        var keys = SortFields.Where(field => fields.Contains(field, StringComparer.OrdinalIgnoreCase)).ToList();
        rows.Sort((left, right) =>
        {
            foreach (var key in keys)
            {
                var comparison = string.Compare(Text(left, key), Text(right, key), StringComparison.Ordinal);
                if (comparison != 0)
                {
                    return comparison;
                }
            }

            return left.Id.CompareTo(right.Id);
        });
    }

    private static List<ElementCategoryCount> CountCategories(
        IReadOnlyList<PreparedQueryRecord> rows,
        IReadOnlyList<string> fields,
        IReadOnlyDictionary<string, string> builtInByCategory)
    {
        if (!fields.Contains("category", StringComparer.OrdinalIgnoreCase))
        {
            return new List<ElementCategoryCount>();
        }

        return rows
            .GroupBy(row => Text(row, "category"), StringComparer.Ordinal)
            .Select(group => new ElementCategoryCount
            {
                Category = group.Key,
                BuiltInCategory = builtInByCategory.GetValueOrDefault(group.Key),
                Count = group.Count()
            })
            .OrderByDescending(entry => entry.Count)
            .ThenBy(entry => entry.Category, StringComparer.Ordinal)
            .ToList();
    }

    private static XlsxCell Cell(PreparedQueryRecord record, string field)
    {
        if (!record.Values.TryGetValue(field, out var value))
        {
            return default;
        }

        // The identifier column carries the number so the column sorts and filters as a number.
        return string.Equals(field, "id", StringComparison.OrdinalIgnoreCase) && value.Number is not null
            ? XlsxCell.FromNumber(value.Number.Value)
            : XlsxCell.FromText(value.Text);
    }

    private static string Text(PreparedQueryRecord record, string field)
    {
        return record.Values.TryGetValue(field, out var value) ? value.Text ?? string.Empty : string.Empty;
    }

    private static string Header(string field)
    {
        return HeaderLabels.TryGetValue(field, out var label) ? label : field;
    }

    private static string ResolvePath(Document document, string? saveTo)
    {
        if (!string.IsNullOrWhiteSpace(saveTo))
        {
            var requested = Path.GetFullPath(saveTo);
            if (File.Exists(requested))
            {
                throw new IOException($"The export file already exists: {requested}.");
            }

            var directory = Path.GetDirectoryName(requested);
            if (!string.IsNullOrEmpty(directory))
            {
                Directory.CreateDirectory(directory);
            }

            return requested;
        }

        var exportDirectory = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments),
            "RevitModelMcp",
            ExportFolder);
        Directory.CreateDirectory(exportDirectory);

        var modelName = string.IsNullOrWhiteSpace(document.PathName)
            ? document.Title
            : Path.GetFileNameWithoutExtension(document.PathName);
        var stamp = DateTime.Now.ToString("yyyyMMdd_HHmmss", CultureInfo.InvariantCulture);
        return Path.Combine(exportDirectory, $"构件ID清单_{Sanitize(modelName)}_{stamp}.xlsx");
    }

    private static string Sanitize(string value)
    {
        var invalid = Path.GetInvalidFileNameChars();
        var cleaned = new string(value.Select(character => invalid.Contains(character) ? '_' : character).ToArray());
        return string.IsNullOrWhiteSpace(cleaned) ? "model" : cleaned.Trim();
    }
}
