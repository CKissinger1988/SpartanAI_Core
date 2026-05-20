using System;
using System.Threading.Tasks;
using Grpc.Net.Client;
using Jarvis;
using Grpc.Core;

class Program
{
    private static string _adminToken = "";
    private static string _clientId = "windows-pc-01";

    static async Task Main(string[] args)
    {
        var channel = GrpcChannel.ForAddress("https://your-cloud-server:50051");
        var client = new JarvisService.JarvisServiceClient(channel);

        while (true)
        {
            Console.WriteLine("\n--- JarvisAI Operational Interface ---");
            Console.WriteLine("1. Standard Command (Metered)");
            Console.WriteLine("2. Switch to Master Admin");
            Console.WriteLine("3. Adaptive Self-Evolution (Master Admin)");
            Console.WriteLine("4. Inject Knowledge (Master Admin)");
            Console.WriteLine("5. Billing & Pi Refill");
            Console.WriteLine("6. Exit");
            Console.Write("Selection: ");
            var choice = Console.ReadLine();

            if (choice == "1") await StartOperationStream(client);
            else if (choice == "2") await HandleElevation(client);
            else if (choice == "3") await HandleEvolution(client);
            else if (choice == "4") await HandleKnowledgeInjection(client);
            else if (choice == "5") await HandleBilling(client);
            else if (choice == "6") break;
        }
    }

    static async Task HandleBilling(JarvisService.JarvisServiceClient client)
    {
        var stats = await client.GetUsageStatsAsync(new UsageRequest { ClientId = _clientId });
        Console.WriteLine($"\n--- Billing Status ---");
        Console.WriteLine($"Current Balance: {stats.CurrentBalance:F2} Credits");
        Console.WriteLine($"Requests Processed: {stats.RequestsProcessed}");
        Console.WriteLine($"Refill Cost: {stats.PiEquivalent:F4} Pi");
        
        Console.Write("\nInitiate Pi Refill? (y/n): ");
        if (Console.ReadLine()?.ToLower() == "y")
        {
            Console.Write("Enter Pi Payment ID: "); var payId = Console.ReadLine();
            Console.Write("Enter Blockchain TxID: "); var txid = Console.ReadLine();
            
            var res = await client.RefillCreditsAsync(new RefillRequest { 
                ClientId = _clientId, PaymentId = payId, Txid = txid 
            });
            
            if (res.Success) Console.WriteLine($"[SUCCESS] Balance refilled to {res.NewBalance} credits.");
            else Console.WriteLine("[FAILED] Payment verification failed.");
        }
    }

    static async Task HandleElevation(JarvisService.JarvisServiceClient client)
    {
        Console.Write("Enter Master Admin Key: ");
        var key = Console.ReadLine();
        var response = await client.ElevatePrivilegesAsync(new ElevationRequest { ClientId = _clientId, MasterKey = key });
        if (response.Success) { _adminToken = response.AdminToken; Console.WriteLine("[SUCCESS] Master Admin mode activated."); }
        else Console.WriteLine($"[FAILED] {response.Message}");
    }

    static async Task HandleEvolution(JarvisService.JarvisServiceClient client)
    {
        if (string.IsNullOrEmpty(_adminToken)) { Console.WriteLine("Error: Must be Master Admin."); return; }
        Console.Write("Target Module: "); var mod = Console.ReadLine();
        Console.WriteLine("Code (End with empty line):");
        string code = ""; string line;
        while (!string.IsNullOrEmpty(line = Console.ReadLine())) { code += line + "\n"; }
        var res = await client.SelfEvolveAsync(new EvolutionCode { AdminToken = _adminToken, LogicSnippet = code, TargetModule = mod });
        Console.WriteLine(res.Success ? "[SUCCESS]" : "[FAILED]");
    }

    static async Task HandleKnowledgeInjection(JarvisService.JarvisServiceClient client)
    {
        if (string.IsNullOrEmpty(_adminToken)) { Console.WriteLine("Error: Must be Master Admin."); return; }
        Console.Write("Brain Side (LIGHT/SHADOW): "); var side = Console.ReadLine()?.ToUpper();
        Console.Write("Tags (comma separated): "); var tags = Console.ReadLine();
        Console.WriteLine("Content (End with empty line):");
        string content = ""; string line;
        while (!string.IsNullOrEmpty(line = Console.ReadLine())) { content += line + "\n"; }

        var res = await client.StoreKnowledgeAsync(new KnowledgeEntry { 
            AdminToken = _adminToken, Side = side, Content = content, Tags = tags 
        });
        Console.WriteLine(res.Success ? $"[SUCCESS] {res.Message}" : "[FAILED]");
    }

    static async Task StartOperationStream(JarvisService.JarvisServiceClient client)
    {
        var headers = new Metadata();
        if (!string.IsNullOrEmpty(_adminToken)) headers.Add("admin-token", _adminToken);
        using var call = client.StreamOperator(headers);
        Console.WriteLine("Stream open. Type 'back' to return.");
        while (true)
        {
            Console.Write("> "); var cmd = Console.ReadLine();
            if (cmd?.ToLower() == "back") break;
            await call.RequestStream.WriteAsync(new OperatorRequest { ClientId = _clientId, Command = cmd });
            if (await call.ResponseStream.MoveNext(default)) Console.WriteLine($"Jarvis: {call.ResponseStream.Current.Message}");
        }
    }
}
