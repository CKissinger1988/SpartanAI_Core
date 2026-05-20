using System;
using System.Threading.Tasks;
using Grpc.Net.Client;
using Jarvis;
using Grpc.Core;

class Program
{
    private static string _adminToken = "";

    static async Task Main(string[] args)
    {
        var channel = GrpcChannel.ForAddress("https://your-cloud-server:50051");
        var client = new JarvisService.JarvisServiceClient(channel);

        Console.WriteLine("--- JarvisAI Operational Interface ---");
        Console.WriteLine("1. Standard Command");
        Console.WriteLine("2. Switch to Master Admin");
        Console.WriteLine("3. Adaptive Self-Evolution (Master Admin Only)");
        Console.Write("Selection: ");
        var choice = Console.ReadLine();

        if (choice == "2") await HandleElevation(client);
        if (choice == "3") await HandleEvolution(client);

        await StartOperationStream(client);
    }

    static async Task HandleElevation(JarvisService.JarvisServiceClient client)
    {
        Console.Write("Enter Master Admin Key: ");
        var key = Console.ReadLine();
        var response = await client.ElevatePrivilegesAsync(new ElevationRequest { ClientId = "windows-pc-01", MasterKey = key });
        if (response.Success) { _adminToken = response.AdminToken; Console.WriteLine("[SUCCESS] Master Admin mode activated."); }
        else Console.WriteLine($"[FAILED] {response.Message}");
    }

    static async Task HandleEvolution(JarvisService.JarvisServiceClient client)
    {
        if (string.IsNullOrEmpty(_adminToken)) { Console.WriteLine("Error: Must be Master Admin to trigger evolution."); return; }
        
        Console.WriteLine("Enter Target Module (e.g., defense, intel):");
        var module = Console.ReadLine();
        Console.WriteLine("Paste New Python Logic Snippet (End with empty line):");
        string code = ""; string line;
        while (!string.IsNullOrEmpty(line = Console.ReadLine())) { code += line + "\n"; }

        var response = await client.SelfEvolveAsync(new EvolutionCode { 
            AdminToken = _adminToken, 
            LogicSnippet = code, 
            TargetModule = module 
        });

        if (response.Success) Console.WriteLine($"[SUCCESS] Evolution Complete: {response.Logs}");
        else Console.WriteLine($"[FAILED] {response.Logs}");
    }

    static async Task StartOperationStream(JarvisService.JarvisServiceClient client)
    {
        var headers = new Metadata();
        if (!string.IsNullOrEmpty(_adminToken)) headers.Add("admin-token", _adminToken);

        using var call = client.StreamOperator(headers);
        Console.WriteLine("Operational stream open.");
        while (true)
        {
            Console.Write("> ");
            var cmd = Console.ReadLine();
            if (cmd?.ToLower() == "exit") break;
            await call.RequestStream.WriteAsync(new OperatorRequest { ClientId = "windows-pc-01", Command = cmd });
            if (await call.ResponseStream.MoveNext(default)) Console.WriteLine($"Jarvis: {call.ResponseStream.Current.Message}");
        }
    }
}
