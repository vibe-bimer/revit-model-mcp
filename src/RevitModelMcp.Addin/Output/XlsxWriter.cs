using System.Globalization;
using System.IO;
using System.IO.Compression;
using System.Text;

namespace RevitModelMcp.Output;

/// <summary>
/// Writes one flat worksheet as a real xlsx package without an Excel library.
/// An xlsx file is a zip of XML parts, which <see cref="ZipArchive"/> and a text writer already cover.
/// Strings use inline storage, so the package needs no shared string table.
/// </summary>
internal sealed class XlsxSheet
{
    private const string SpreadsheetNamespace = "http://schemas.openxmlformats.org/spreadsheetml/2006/main";
    private const string RelationshipNamespace = "http://schemas.openxmlformats.org/officeDocument/2006/relationships";
    private const string PackageRelationshipNamespace = "http://schemas.openxmlformats.org/package/2006/relationships";
    private const string ContentTypeNamespace = "http://schemas.openxmlformats.org/package/2006/content-types";

    private static readonly UTF8Encoding Utf8WithoutBom = new(false);

    private readonly string _name;
    private readonly IReadOnlyList<string> _headers;
    private readonly IReadOnlyList<int> _columnWidths;
    private readonly List<IReadOnlyList<XlsxCell>> _rows = new();

    internal XlsxSheet(string name, IReadOnlyList<string> headers, IReadOnlyList<int> columnWidths)
    {
        _name = name;
        _headers = headers;
        _columnWidths = columnWidths;
    }

    internal int RowCount => _rows.Count;

    internal void AddRow(IReadOnlyList<XlsxCell> cells)
    {
        _rows.Add(cells);
    }

    internal void Save(string path)
    {
        using var stream = new FileStream(path, FileMode.CreateNew, FileAccess.Write, FileShare.None);
        using var archive = new ZipArchive(stream, ZipArchiveMode.Create);
        WritePart(archive, "[Content_Types].xml", ContentTypesXml());
        WritePart(archive, "_rels/.rels", RootRelationshipsXml());
        WritePart(archive, "xl/workbook.xml", WorkbookXml());
        WritePart(archive, "xl/_rels/workbook.xml.rels", WorkbookRelationshipsXml());
        WritePart(archive, "xl/styles.xml", StylesXml());
        WritePart(archive, "xl/worksheets/sheet1.xml", WorksheetXml());
    }

    private static void WritePart(ZipArchive archive, string entryName, string content)
    {
        var entry = archive.CreateEntry(entryName, CompressionLevel.Optimal);
        using var writer = new StreamWriter(entry.Open(), Utf8WithoutBom);
        writer.Write(content);
    }

    private string WorksheetXml()
    {
        var lastColumn = ColumnName(_headers.Count - 1);
        var lastRow = _rows.Count + 1;
        var builder = new StringBuilder();
        builder.Append("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>");
        builder.Append($"<worksheet xmlns=\"{SpreadsheetNamespace}\">");
        builder.Append($"<dimension ref=\"A1:{lastColumn}{lastRow}\"/>");
        builder.Append("<sheetViews><sheetView tabSelected=\"1\" workbookViewId=\"0\">");
        // The header stays visible while the list scrolls.
        builder.Append("<pane ySplit=\"1\" topLeftCell=\"A2\" activePane=\"bottomLeft\" state=\"frozen\"/>");
        builder.Append("<selection pane=\"bottomLeft\" activeCell=\"A2\" sqref=\"A2\"/>");
        builder.Append("</sheetView></sheetViews>");
        builder.Append("<sheetFormatPr defaultRowHeight=\"15\"/>");
        builder.Append("<cols>");
        for (var index = 0; index < _columnWidths.Count; index++)
        {
            builder.Append($"<col min=\"{index + 1}\" max=\"{index + 1}\" width=\"{_columnWidths[index]}\" customWidth=\"1\"/>");
        }

        builder.Append("</cols><sheetData>");
        builder.Append("<row r=\"1\">");
        for (var index = 0; index < _headers.Count; index++)
        {
            builder.Append($"<c r=\"{ColumnName(index)}1\" s=\"1\" t=\"inlineStr\"><is><t>{Escape(_headers[index])}</t></is></c>");
        }

        builder.Append("</row>");
        for (var rowIndex = 0; rowIndex < _rows.Count; rowIndex++)
        {
            var rowNumber = rowIndex + 2;
            builder.Append($"<row r=\"{rowNumber}\">");
            var cells = _rows[rowIndex];
            for (var index = 0; index < cells.Count; index++)
            {
                var cell = cells[index];
                var reference = $"{ColumnName(index)}{rowNumber}";
                if (cell.Text is not null)
                {
                    builder.Append($"<c r=\"{reference}\" t=\"inlineStr\"><is><t xml:space=\"preserve\">{Escape(cell.Text)}</t></is></c>");
                }
                else if (cell.Number is not null)
                {
                    builder.Append($"<c r=\"{reference}\"><v>{cell.Number.Value.ToString("R", CultureInfo.InvariantCulture)}</v></c>");
                }

                // A cell with neither value stays absent, which Excel reads as empty.
            }

            builder.Append("</row>");
        }

        builder.Append("</sheetData>");
        builder.Append($"<autoFilter ref=\"A1:{lastColumn}{lastRow}\"/>");
        builder.Append("</worksheet>");
        return builder.ToString();
    }

    private string WorkbookXml()
    {
        return "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
               $"<workbook xmlns=\"{SpreadsheetNamespace}\" xmlns:r=\"{RelationshipNamespace}\">" +
               $"<sheets><sheet name=\"{Escape(_name)}\" sheetId=\"1\" r:id=\"rId1\"/></sheets>" +
               "</workbook>";
    }

    private static string WorkbookRelationshipsXml()
    {
        return "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
               $"<Relationships xmlns=\"{PackageRelationshipNamespace}\">" +
               $"<Relationship Id=\"rId1\" Type=\"{RelationshipNamespace}/worksheet\" Target=\"worksheets/sheet1.xml\"/>" +
               $"<Relationship Id=\"rId2\" Type=\"{RelationshipNamespace}/styles\" Target=\"styles.xml\"/>" +
               "</Relationships>";
    }

    private static string RootRelationshipsXml()
    {
        return "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
               $"<Relationships xmlns=\"{PackageRelationshipNamespace}\">" +
               $"<Relationship Id=\"rId1\" Type=\"{RelationshipNamespace}/officeDocument\" Target=\"xl/workbook.xml\"/>" +
               "</Relationships>";
    }

    private static string ContentTypesXml()
    {
        return "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
               $"<Types xmlns=\"{ContentTypeNamespace}\">" +
               "<Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>" +
               "<Default Extension=\"xml\" ContentType=\"application/xml\"/>" +
               "<Override PartName=\"/xl/workbook.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml\"/>" +
               "<Override PartName=\"/xl/worksheets/sheet1.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml\"/>" +
               "<Override PartName=\"/xl/styles.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml\"/>" +
               "</Types>";
    }

    private static string StylesXml()
    {
        // Two formats only: the default one and a bold shaded header.
        return "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" +
               $"<styleSheet xmlns=\"{SpreadsheetNamespace}\">" +
               "<fonts count=\"2\"><font><sz val=\"11\"/><name val=\"Calibri\"/></font>" +
               "<font><b/><sz val=\"11\"/><name val=\"Calibri\"/></font></fonts>" +
               "<fills count=\"3\"><fill><patternFill patternType=\"none\"/></fill>" +
               "<fill><patternFill patternType=\"gray125\"/></fill>" +
               "<fill><patternFill patternType=\"solid\"><fgColor rgb=\"FFD9E1F2\"/><bgColor indexed=\"64\"/></patternFill></fill></fills>" +
               "<borders count=\"1\"><border><left/><right/><top/><bottom/><diagonal/></border></borders>" +
               "<cellStyleXfs count=\"1\"><xf numFmtId=\"0\" fontId=\"0\" fillId=\"0\" borderId=\"0\"/></cellStyleXfs>" +
               "<cellXfs count=\"2\"><xf numFmtId=\"0\" fontId=\"0\" fillId=\"0\" borderId=\"0\" xfId=\"0\"/>" +
               "<xf numFmtId=\"0\" fontId=\"1\" fillId=\"2\" borderId=\"0\" xfId=\"0\" applyFont=\"1\" applyFill=\"1\"/></cellXfs>" +
               "<cellStyles count=\"1\"><cellStyle name=\"Normal\" xfId=\"0\" builtinId=\"0\"/></cellStyles>" +
               "</styleSheet>";
    }

    private static string ColumnName(int index)
    {
        var name = string.Empty;
        var value = index;
        while (true)
        {
            name = (char)('A' + value % 26) + name;
            value = value / 26 - 1;
            if (value < 0)
            {
                return name;
            }
        }
    }

    private static readonly char[] XmlSpecialCharacters = { '&', '<', '>', '"', '\'' };

    private static string Escape(string value)
    {
        if (value.IndexOfAny(XmlSpecialCharacters) < 0)
        {
            return value;
        }

        // String.Replace(string, string) compares ordinally and is the only overload .NET Framework offers.
        return value
            .Replace("&", "&amp;")
            .Replace("<", "&lt;")
            .Replace(">", "&gt;")
            .Replace("\"", "&quot;")
            .Replace("'", "&apos;");
    }
}

/// <summary>One worksheet cell: text, a number, or nothing.</summary>
internal readonly struct XlsxCell
{
    private XlsxCell(string? text, double? number)
    {
        Text = text;
        Number = number;
    }

    internal string? Text { get; }

    internal double? Number { get; }

    internal static XlsxCell FromText(string? value)
    {
        return string.IsNullOrEmpty(value) ? default : new XlsxCell(value, null);
    }

    internal static XlsxCell FromNumber(double value)
    {
        return new XlsxCell(null, value);
    }
}
