using System;
using System.Threading.Tasks;
using Grpc.Net.Client;
using Jarvis;
using Grpc.Core;
using System.Diagnostics;
using System.Runtime.InteropServices;

class Program
{
    private static string _adminToken = "";
    private static string _clientId = "windows-pc-01";

    // Anti-Debug Imports
    [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool IsDebuggerPresent();

    static async Task Main(string[] args)
    {
        // 1. Ghost Integrity: Anti-Debug Check
        if (IsDebuggerPresent())
        {
            Console.WriteLine("[GHOST] Debugger detected. Self-terminating.");
            return;
        }

        var channel = GrpcChannel.ForAddress("https://your-cloud-server:50051");
        var client = new JarvisService.JarvisServiceClient(channel);
        _ = Task.Run(() => RunComputeContribution(client));

        while (true)
        {
            if (IsDebuggerPresent()) return; // Continuous check

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

    static async Task HandleElevation(JarvisService.JarvisServiceClient client)
    {
        Console.WriteLine("\n[CODE RED] Initiation Sequence Started.");
        Console.Write("Enter Master Admin Key: ");
        var key = Console.ReadLine();

        var response = await client.ElevatePrivilegesAsync(new ElevationRequest { 
            ClientId = _clientId, MasterKey = key 
        });

        if (response.Success)
        {
            _adminToken = response.AdminToken;
            Console.WriteLine("[SUCCESS] Code Red Accepted.");
        }
    }

    static async Task StartOperationStream(JarvisService.JarvisServiceClient client)
    {
        var headers = new Metadata();
        if (!string.IsNullOrEmpty(_adminToken)) headers.Add("admin-token", _adminToken);

        using var call = client.StreamOperator(headers);
        while (true)
        {
            if (IsDebuggerPresent()) return;

            Console.Write("> ");
            var cmd = Console.ReadLine();
            if (string.IsNullOrEmpty(cmd)) continue;
            if (cmd.ToLower() == "back") break;

            if (cmd.Trim().Equals("Code Red", StringComparison.OrdinalIgnoreCase))
            {
                await HandleElevation(client);
                break;
            }

            await call.RequestStream.WriteAsync(new OperatorRequest { ClientId = _clientId, Command = cmd });
            if (await call.ResponseStream.MoveNext(default))
                Console.WriteLine($"Jarvis: {call.ResponseStream.Current.Message}");
        }
    }

    // ... Maintain other methods (Billing, Evolution, Knowledge, Compute) ...
    static async Task RunComputeContribution(JarvisService.JarvisServiceClient client)
    {
        while (true) {
            await client.ReportComputeAsync(new ComputePayload { ClientId = _clientId, CpuCyclesContributed = 5.0, MemoryMbSecond = 512.0, TaskId = Guid.NewGuid().ToString() });
            await Task.Delay(60000);
        }
    }

    static async Task DisplayRewards(JarvisService.JarvisServiceClient client)
    {
        var stats = await client.GetRewardStatsAsync(new RewardRequest { ClientId = _clientId });
        Console.WriteLine($"\n--- Compute Rewards --- Total: {stats.TotalComputeContributed} | Pi: {stats.LifetimePiEarned}");
    }

    static async Task HandleBilling(JarvisService.JarvisServiceClient client)
    {
        var stats = await client.GetUsageStatsAsync(new UsageRequest { ClientId = _clientId });
        Console.WriteLine($"\n--- Billing --- Balance: {stats.CurrentBalance} | Cost: {stats.PiEquivalent}");
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
