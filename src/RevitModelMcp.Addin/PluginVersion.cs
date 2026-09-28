using System.Diagnostics;
using System.Reflection;

namespace RevitModelMcp;

/// <summary>
/// Identifies the add-in build that answers a request, so a response tells the Revit year and the
/// plug-in build apart. The release pipeline stamps the product version, for example
/// <c>0.6.0+68febc5dc6c56cd2ed7eb3ecb6905b6adc5cb84e</c>.
/// </summary>
internal static class PluginVersion
{
    public static string Value { get; } = Resolve();

    private static string Resolve()
    {
        var assembly = typeof(PluginVersion).Assembly;
        try
        {
            var location = assembly.Location;
            if (!string.IsNullOrEmpty(location))
            {
                var product = FileVersionInfo.GetVersionInfo(location).ProductVersion;
                if (!string.IsNullOrWhiteSpace(product))
                {
                    return product;
                }
            }
        }
        catch (Exception)
        {
            // Version reporting must never interrupt add-in loading.
        }

        return assembly.GetName().Version?.ToString() ?? "unknown";
    }
}
