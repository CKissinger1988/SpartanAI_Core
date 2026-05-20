using System;
using System.Threading.Tasks;
using Grpc.Net.Client;
using Jarvis;
using Grpc.Core;
using System.Diagnostics;

class Program
{
    private static string _adminToken = "";
    private static string _clientId = "windows-pc-01";

    static async Task Main(string[] args)
    {
        var channel = GrpcChannel.ForAddress("https://your-cloud-server:50051");
        var client = new JarvisService.JarvisServiceClient(channel);

        // Start Background Compute Contribution Task
        _ = Task.Run(() => RunComputeContribution(client));

        while (true)
        {
            Console.WriteLine("\n--- JarvisAI Operational Interface ---");
            Console.WriteLine("1. Standard Command (Metered)");
            Console.WriteLine("2. Switch to Master Admin (Code Red)");
            Console.WriteLine("3. Adaptive Self-Evolution (Master Admin)");
            Console.WriteLine("4. Inject Knowledge (Master Admin)");
            Console.WriteLine("5. Billing & Pi Refill");
            Console.WriteLine("6. Compute Reward Stats");
            Console.WriteLine("7. Exit");
            Console.Write("Selection: ");
            var choice = Console.ReadLine();

            if (choice == "1") await StartOperationStream(client);
            else if (choice == "2") await HandleElevation(client);
            else if (choice == "3") await HandleEvolution(client);
            else if (choice == "4") await HandleKnowledgeInjection(client);
            else if (choice == "5") await HandleBilling(client);
            else if (choice == "6") await DisplayRewards(client);
            else if (choice == "7") break;
        }
    }

    static async Task RunComputeContribution(JarvisService.JarvisServiceClient client)
    {
        while (true)
        {
            double cpuContribution = new Random().NextDouble() * 10;
            double memContribution = 512.0;

            await client.ReportComputeAsync(new ComputePayload {
                ClientId = _clientId,
                CpuCyclesContributed = cpuContribution,
                MemoryMbSecond = memContribution,
                TaskId = Guid.NewGuid().ToString()
            });

            await Task.Delay(60000);
        }
    }

    static async Task DisplayRewards(JarvisService.JarvisServiceClient client)
    {
        var stats = await client.GetRewardStatsAsync(new RewardRequest { ClientId = _clientId });
        Console.WriteLine($"\n--- Compute Rewards ---");
        Console.WriteLine($"Total Compute Contributed: {stats.TotalComputeContributed:F2} Units");
        Console.WriteLine($"Lifetime Pi Earned: {stats.LifetimePiEarned:F6} Pi");
        Console.WriteLine($"Pending Payout: {stats.PendingPiPayout:F6} Pi");
    }

    static async Task HandleElevation(JarvisService.JarvisServiceClient client)
    {
        Console.WriteLine("\n[CODE RED] Initiation Sequence Started.");
        Console.Write("Enter Master Admin Key: ");
        var key = Console.ReadLine();

        var response = await client.ElevatePrivilegesAsync(new ElevationRequest { 
            ClientId = _clientId, 
            MasterKey = key 
        });

        if (response.Success)
        {
            _adminToken = response.AdminToken;
            Console.WriteLine("[SUCCESS] Code Red Accepted. Master Admin mode activated.");
        }
        else
        {
            Console.WriteLine($"[FAILED] Code Red Denied. {response.Message}");
        }
    }

    static async Task StartOperationStream(JarvisService.JarvisServiceClient client)
    {
        var headers = new Metadata();
        if (!string.IsNullOrEmpty(_adminToken)) headers.Add("admin-token", _adminToken);

        using var call = client.StreamOperator(headers);
        Console.WriteLine("Operational stream open. Type 'back' to return.");
        
        while (true)
        {
            Console.Write("> ");
            var cmd = Console.ReadLine();
            if (string.IsNullOrEmpty(cmd)) continue;
            if (cmd.ToLower() == "back") break;

            // Trigger "Code Red" elevation from within the command stream
            if (cmd.Trim().Equals("Code Red", StringComparison.OrdinalIgnoreCase))
            {
                await HandleElevation(client);
                // Restart stream to apply new token
                break;
            }

            await call.RequestStream.WriteAsync(new OperatorRequest { ClientId = _clientId, Command = cmd });
            
            if (await call.ResponseStream.MoveNext(default))
            {
                var response = call.ResponseStream.Current;
                Console.WriteLine($"Jarvis: {response.Message}");
            }
        }
    }

    // ... Maintain HandleBilling, HandleEvolution, HandleKnowledgeInjection ...
    static async Task HandleBilling(JarvisService.JarvisServiceClient client)
    {
        var stats = await client.GetUsageStatsAsync(new UsageRequest { ClientId = _clientId });
        Console.WriteLine($"\n--- Billing Status --- Balance: {stats.CurrentBalance:F2} | Refill: {stats.PiEquivalent:F4} Pi");
    }

    static async Task HandleEvolution(JarvisService.JarvisServiceClient client)
    {
        if (string.IsNullOrEmpty(_adminToken)) return;
        Console.Write("Mod: "); var m = Console.ReadLine();
        string c = ""; string l; while (!string.IsNullOrEmpty(l = Console.ReadLine())) { c += l + "\n"; }
        await client.SelfEvolveAsync(new EvolutionCode { AdminToken = _adminToken, LogicSnippet = c, TargetModule = m });
    }

    static async Task HandleKnowledgeInjection(JarvisService.JarvisServiceClient client)
    {
        if (string.IsNullOrEmpty(_adminToken)) return;
        Console.Write("Side: "); var s = Console.ReadLine();
        Console.Write("Tags: "); var t = Console.ReadLine();
        string c = ""; string l; while (!string.IsNullOrEmpty(l = Console.ReadLine())) { c += l + "\n"; }
        await client.StoreKnowledgeAsync(new KnowledgeEntry { AdminToken = _adminToken, Side = s, Content = c, Tags = t });
    }
}
