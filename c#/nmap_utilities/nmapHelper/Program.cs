using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Xml;
using System.Xml.Linq;

public class nmapHelper {
    public static void Main(string[] args) {
        // Get the path to the XML file and XSLT file.
        string xPath = args[0];
        IEnumerable<HostPort> hostPorts = ParseNmapXML(xPath);
        foreach (var hostPort in hostPorts) {
            foreach (var port in hostPort.Ports) {
                Console.WriteLine(hostPort.Address + ":" + port);
            }
        }
    }

    public static IEnumerable<HostPort> ParseNmapXML(string filepath) {
        var document = XElement.Load(filepath);// XmlDocumentLoader.LoadXmlDocumentFromFilepath(filepath);
        var hosts = document.Elements("host");
        foreach (var host in hosts) {
            if ("up".Equals(host.Element("status").Attribute("state").Value)) {
                var address = host.Element("address").Attribute("addr").Value;
                var ports = host.Element("ports").Elements("port").Select(port => port.Attribute("portid").Value);
                yield return new HostPort(address, ports);
            }
        }
    }
}
public class XmlDocumentLoader {
    public static XmlDocument LoadXmlDocumentFromFilepath(string filepath) {
        if (File.Exists(filepath)) {
            try {
                XmlDocument xmlDocument = new XmlDocument();
                xmlDocument.Load(filepath);
                return xmlDocument;
            }
            catch {
                throw new Exception("Document was not XML");
            }
        }
        else {
            throw new FileNotFoundException("The filepath provided does not exist");
        }
            
    }
}
public class HostPort {
    public string Address { get; private set; }
    public IEnumerable<string> Ports { get; private set; }
    public HostPort(string address, IEnumerable<string> ports) {
        Address = address;
        Ports = ports;
    }
}