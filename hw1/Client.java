import java.util.Scanner;
import java.net.*;
import java.io.*;

public class Client {
  public static void main(String[] args) {
    String hostAddress;
    int tcpPort;
    int udpPort;
    PrintWriter out = null;
    BufferedReader in = null;

    if (args.length != 3) {
      System.out.println("ERROR: Provide 3 arguments");
      System.out.println("\t(1) <hostAddress>: the address of the server");
      System.out.println("\t(2) <tcpPort>: the port number for TCP connection");
      System.out.println("\t(3) <udpPort>: the port number for UDP connection");
      System.exit(-1);
    }

    hostAddress = args[0];
    tcpPort = Integer.parseInt(args[1]);
    udpPort = Integer.parseInt(args[2]);

    // Setup the Socket to the server
    try (Socket socket = new Socket(hostAddress, tcpPort)) {
      Scanner sc = new Scanner(System.in);
      out = new PrintWriter(socket.getOutputStream(), true);
      in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
      String serverResponse;

      while (sc.hasNextLine()) {
        String cmd = sc.nextLine();
        String[] tokens = cmd.split(" ");

        if (tokens[0].equals("setmode")) {
          // TODO: set the mode of communication for sending commands to the server
          // and display the name of the protocol that will be used in future
        } else if (tokens[0].equals("purchase")) {
          if (tokens.length != 4) {
            continue;
          }
          try {
            Integer.parseInt(tokens[3]);
          } catch (NumberFormatException nfe) {
            System.out.println("Purchase Quantity not an Int");
            continue;
          }
          out.println(cmd);
        } else if (tokens[0].equals("cancel")) {
          if (tokens.length != 2) {
            continue;
          }
          try {
            Integer.parseInt(tokens[1]);
          } catch (NumberFormatException nfe) {
            System.out.println("Order Number not an Int");
            continue;
          }
          out.println(cmd);
        } else if (tokens[0].equals("search")) {
          if (tokens.length != 2) {
            continue;
          }
          out.println(cmd);
        } else if (tokens[0].equals("list")) {
          if (tokens.length != 1) {
            continue;
          }
          out.println(cmd);
        } else {
          System.out.println("ERROR: No such command");
          continue;
        }

        // Print out the server response
        while (((serverResponse = in.readLine()) != null) && (!serverResponse.equals("EOR"))) {
          System.out.println(serverResponse);
        }
      }
    } catch (UnknownHostException ex) {
      System.out.println("Server not found: " + ex.getMessage());
    } catch (IOException ex) {
      System.out.println("I/O error: " + ex.getMessage());
    }

  }
}
