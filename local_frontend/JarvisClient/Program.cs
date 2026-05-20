using System;
using System.Threading.Tasks;
using Grpc.Net.Client;
using Jarvis;
using Grpc.Core;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Net.Http;
using System.Security.Cryptography.X509Certificates;

class Program
{
    private static string _adminToken = "";
    private static string _clientId = "supreme-operator-pc";

    [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool IsDebuggerPresent();

    static async Task Main(string[] args)
    {
        // 1. Ghost Integrity
        if (IsDebuggerPresent()) return;

        Console.Title = "JarvisAI Grand Synthesis Operator";
        Console.ForegroundColor = ConsoleColor.Cyan;
        Console.WriteLine("--- Initializing Secure Link to Supreme Core ---");

        try {
            // 2. Configure mTLS Channel
            var handler = new HttpClientHandler();
            // In production, load from 'certs' folder
            // handler.ClientCertificates.Add(new X509Certificate2("certs/client.pfx", "password"));
            
            var channel = GrpcChannel.ForAddress("https://your-cloud-server:50051", new GrpcChannelOptions {
                HttpHandler = handler
            });
            var client = new JarvisService.JarvisServiceClient(channel);

            _ = Task.Run(() => RunComputeContribution(client));

            while (true)
            {
                if (IsDebuggerPresent()) return;

                Console.ResetColor();
                Console.WriteLine("\n--- JARVISAI OPERATIONAL CONSOLE ---");
                Console.WriteLine("1. [METERED] Operational Stream");
                Console.WriteLine("2. [OVERRIDE] CODE RED");
                Console.WriteLine("3. [ADAPT] Core Evolution");
                Console.WriteLine("4. [INTELLIGENCE] Inject Knowledge");
                Console.WriteLine("5. [ECONOMY] Billing & Rewards");
                Console.WriteLine("6. [SEARCH] Global Intelligence Query");
                Console.WriteLine("7. Exit");
                Console.Write("Selection: ");
                var choice = Console.ReadLine();

                switch (choice)
                {
                    case "1": await StartOperationStream(client); break;
                    case "2": await HandleCodeRed(client); break;
                    case "3": await HandleEvolution(client); break;
                    case "4": await HandleKnowledgeInjection(client); break;
                    case "5": await DisplayBillingAndRewards(client); break;
                    case "6": await HandleGlobalSearch(client); break;
                    case "7": return;
                }
            }
        } catch (Exception ex) {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"FATAL: Link severed. {ex.Message}");
        }
    }

    static async Task HandleCodeRed(JarvisService.JarvisServiceClient client)
    {
        Console.ForegroundColor = ConsoleColor.Red;
        Console.WriteLine("\n--- CODE RED: INITIATING SUPREME ELEVATION ---");
        Console.Write("Enter Master Key: ");
        var key = Console.ReadLine();

        var res = await client.ElevatePrivilegesAsync(new ElevationRequest { ClientId = _clientId, MasterKey = key });
        if (res.Success) {
            _adminToken = res.AdminToken;
            Console.WriteLine($"[SUCCESS]: {res.Message}");
        } else {
            Console.WriteLine("[FAILED]: Supreme authority rejected.");
        }
    }

    static async Task HandleGlobalSearch(JarvisService.JarvisServiceClient client)
    {
        Console.Write("\nEnter search vector: ");
        var query = Console.ReadLine();
        var res = await client.GlobalSearchAsync(new IntelligenceQuery { SearchVector = query });
        Console.ForegroundColor = ConsoleColor.Yellow;
        Console.WriteLine(res.Synthesis);
    }

    static async Task StartOperationStream(JarvisService.JarvisServiceClient client)
    {
        var headers = new Metadata();
        if (!string.IsNullOrEmpty(_adminToken)) headers.Add("admin-token", _adminToken);

        using var call = client.StreamOperator(headers);
        Console.WriteLine("Operational stream open. Code Red active within stream.");
        
        while (true)
        {
            if (IsDebuggerPresent()) return;
            Console.Write("> ");
            var cmd = Console.ReadLine();
            if (cmd?.ToLower() == "back") break;
            if (cmd?.Equals("Code Red", StringComparison.OrdinalIgnoreCase) == true) { await HandleCodeRed(client); break; }

            await call.RequestStream.WriteAsync(new OperatorRequest { ClientId = _clientId, Command = cmd });
            if (await call.ResponseStream.MoveNext(default))
                Console.WriteLine($"J: {call.ResponseStream.Current.Message}");
        }
    }

    static async Task DisplayBillingAndRewards(JarvisService.JarvisServiceClient client)
    {
        var b = await client.GetUsageStatsAsync(new UsageRequest { ClientId = _clientId });
        var r = await client.GetRewardStatsAsync(new RewardRequest { ClientId = _clientId });
        Console.WriteLine($"\n--- ECONOMY STATUS ---");
        Console.WriteLine($"Balance: {b.CurrentBalance:F2} | Earnings: {r.LifetimePiEarned:F6} Pi");
    }

    static async Task RunComputeContribution(JarvisService.JarvisServiceClient client)
    {
        while (true) {
            try { await client.ReportComputeAsync(new ComputePayload { ClientId = _clientId, CpuCyclesContributed = 10.0, MemoryMbSecond = 1024, TaskId = Guid.NewGuid().ToString() }); } catch {}
            await Task.Delay(60000);
        }
    }

    static async Task HandleEvolution(JarvisService.JarvisServiceClient client)
    {
        if (string.IsNullOrEmpty(_adminToken)) return;
        Console.Write("Module: "); var m = Console.ReadLine();
        string c = ""; string l; while (!string.IsNullOrEmpty(l = Console.ReadLine())) { c += l + "\n"; }
        var res = await client.SelfEvolveAsync(new EvolutionCode { AdminToken = _adminToken, LogicSnippet = c, TargetModule = m });
        Console.WriteLine(res.Success ? "ADAPTED." : "FAILED.");
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
