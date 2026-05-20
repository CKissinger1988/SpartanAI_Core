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
        // 1. Connect to the cloud backend with mTLS
        // (Assuming certs are available locally in 'certs' folder)
        var channel = GrpcChannel.ForAddress("https://your-cloud-server:50051");
        var client = new JarvisService.JarvisServiceClient(channel);

        Console.WriteLine("--- JarvisAI Operational Interface ---");
        Console.WriteLine("1. Send Standard Command");
        Console.WriteLine("2. Switch to Master Admin");
        Console.Write("Selection: ");
        var choice = Console.ReadLine();

        if (choice == "2")
        {
            await HandleElevation(client);
        }

        await StartOperationStream(client);
    }

    static async Task HandleElevation(JarvisService.JarvisServiceClient client)
    {
        Console.Write("Enter Master Admin Key: ");
        var key = Console.ReadLine();

        var response = await client.ElevatePrivilegesAsync(new ElevationRequest { 
            ClientId = "windows-pc-01", 
            MasterKey = key 
        });

        if (response.Success)
        {
            _adminToken = response.AdminToken;
            Console.WriteLine("[SUCCESS] Master Admin mode activated.");
        }
        else
        {
            Console.WriteLine($"[FAILED] {response.Message}");
        }
    }

    static async Task StartOperationStream(JarvisService.JarvisServiceClient client)
    {
        // Include admin token in metadata if available
        var headers = new Metadata();
        if (!string.IsNullOrEmpty(_adminToken))
        {
            headers.Add("admin-token", _adminToken);
        }

        using var call = client.StreamOperator(headers);

        Console.WriteLine("Enter command (or 'exit' to quit):");
        while (true)
        {
            Console.Write("> ");
            var cmd = Console.ReadLine();
            if (cmd?.ToLower() == "exit") break;

            await call.RequestStream.WriteAsync(new OperatorRequest { 
                ClientId = "windows-pc-01", 
                Command = cmd 
            });

            if (await call.ResponseStream.MoveNext(default))
            {
                var response = call.ResponseStream.Current;
                Console.WriteLine($"Jarvis: {response.Message}");
            }
        }
    }
}
