import java.io.*;
import java.net.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.*;
import java.util.concurrent.locks.ReentrantLock;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;


public class Server {
  static ServerSocket server = null;
  static AtomicInteger orderID = new AtomicInteger(0);
  static ConcurrentHashMap<String, Integer> storeInventory = new ConcurrentHashMap<>();
  static ConcurrentHashMap<Integer, OrderInformation> orderHistory = new ConcurrentHashMap<>();
  static ReentrantLock storeAndOrderLock = new ReentrantLock();
  //Struct to hold order information
  static class OrderInformation
  {
    public String username;
    public String product;
    public int    quantity;
    public OrderInformation(String Username, String Product, int Quantity) {
        username = Username;
        product = Product;
        quantity = Quantity;
    }
    public void print(){
      System.out.println(username + product + quantity);
    }
  };
  
  public static void main (String[] args) {
    int tcpPort;
    int udpPort;
    if (args.length != 3) {
      System.out.println("ERROR: Provide 3 arguments");
      System.out.println("\t(1) <tcpPort>: the port number for TCP connection");
      System.out.println("\t(2) <udpPort>: the port number for UDP connection");
      System.out.println("\t(3) <file>: the file of inventory");

      System.exit(-1);
    }
    tcpPort = Integer.parseInt(args[0]);
    udpPort = Integer.parseInt(args[1]);
    String fileName = args[2];

    // Parse the inventory file into a concurrency safe HashTable
    BufferedReader reader;
		try {
			reader = new BufferedReader(new FileReader(fileName));
			String line = reader.readLine();
			while (line != null) {
				// read next line
        String[] tokens = line.split(" ");
        if(tokens.length != 2){
          break;
        }
        storeInventory.putIfAbsent(tokens[0], Integer.parseInt(tokens[1]));
				line = reader.readLine();
			}
			reader.close();
      System.out.println(storeInventory);
		} catch (IOException e) {
			e.printStackTrace();
		}

    // Setup the server
    try {
            server = new ServerSocket(tcpPort);
            server.setReuseAddress(true);
  
            //Accept client loop
            while (true) {
                Socket client = server.accept();
                System.out.println("New client connected "+ client.getInetAddress().getHostAddress());
  
                // create a new thread for client and start it
                ClientHandler clientSock= new ClientHandler(client);
                new Thread(clientSock).start();
            }
        }
        catch (IOException e) {e.printStackTrace();}
  }

  // Class which handles the client thread
  private static class ClientHandler implements Runnable {
      private final Socket clientSocket;

      // Constructor
      public ClientHandler(Socket socket)
      {
          this.clientSocket = socket;
      }

      public void run()
      {
          PrintWriter out = null;
          BufferedReader in = null;
          try {
              out = new PrintWriter(clientSocket.getOutputStream(), true);
              in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
              String clientRequest;

              //Handling client input loop
              while ((clientRequest = in.readLine()) != null) {
                storeAndOrderLock.lock();
                String[] tokens = clientRequest.split(" ");
                System.out.printf(" Sent from the client: %s\n",clientRequest);
                if (tokens[0].equals("setmode")) {
                  //Todo Implement this function
                }
                else if (tokens[0].equals("purchase")) {
                  Integer quantityRequested = Integer.parseInt(tokens[3]);
                  String productRequested = tokens[2];
                  String requesterUsername = tokens[1];
                  // Check to see if there are enough items to purchase
                  if(storeInventory.containsKey(productRequested)){
                    Integer quantityAvailable = storeInventory.get(productRequested);
                    if(quantityAvailable >= quantityRequested){
                      //Create order
                      orderHistory.put(orderID.getAndIncrement(), new OrderInformation(requesterUsername, productRequested, quantityRequested));
                      //Update Inventory
                      storeInventory.replace(productRequested, quantityAvailable - quantityRequested);
                      out.println("Your order has been placed, "+(orderID.get()-1)+" "+requesterUsername+" "+productRequested+" "+quantityRequested);
                    } else {
                    out.println("Not Available - Not enough items");
                    }
                  } else {
                    out.println("Not Available - We do not sell this product");
                  }
                  // 
                } else if (tokens[0].equals("cancel")) {
                  Integer orderIdToCancel = Integer.parseInt(tokens[1]);
                  // Find the order
                  if(orderHistory.containsKey(orderIdToCancel)){
                    OrderInformation cancelOrderInfo = orderHistory.get(orderIdToCancel);
                    cancelOrderInfo.print();
                    Integer quantityCanceled = cancelOrderInfo.quantity;
                    String productCanceled = cancelOrderInfo.product;
                    Integer currentQuantity = storeInventory.get(productCanceled);
                    storeInventory.replace(productCanceled, currentQuantity + quantityCanceled);
                    orderHistory.remove(orderIdToCancel);
                    out.println("Order "+orderIdToCancel+" is canceled");
                  } else {
                    out.println(orderIdToCancel+" not found, no such order");
                  }
                } else if (tokens[0].equals("search")) {
                  String customerNameToSearch = tokens[1];
                  boolean found = false;
                  for (Map.Entry<Integer, OrderInformation> entry : orderHistory.entrySet()) {
                    Integer key = entry.getKey();
                    OrderInformation value = entry.getValue();
                    if(value.username.equals(customerNameToSearch)){
                      found = true;
                      out.println(key+", "+value.product+", "+value.quantity);
                    }
                  }
                  if(!found){
                    out.println("No order found for "+customerNameToSearch+"");
                  }
                } else if (tokens[0].equals("list")) {
                  for (Map.Entry<String, Integer> entry : storeInventory.entrySet()) {
                    String item = entry.getKey();
                    Integer quantity = entry.getValue();
                    out.println(item+" "+quantity);
                  }
                } else {
                  System.out.println("ERROR: Invalid command send from client");
                }
                storeAndOrderLock.unlock();

                System.out.println(storeInventory);
                System.out.println(orderHistory);
                out.println("EOR");
              }
          }
          catch (IOException e) {e.printStackTrace();}
      }
  }
}
