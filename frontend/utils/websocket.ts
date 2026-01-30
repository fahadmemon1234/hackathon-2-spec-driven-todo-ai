import { toast } from "sonner";

class WebSocketService {
  private static instance: WebSocketService;
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectInterval = 5000; // 5 seconds
  private listeners: Map<string, Function[]> = new Map();
  private isConnected = false;

  private constructor() {}

  public static getInstance(): WebSocketService {
    if (!WebSocketService.instance) {
      WebSocketService.instance = new WebSocketService();
    }
    return WebSocketService.instance;
  }

  public connect(userId?: string) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      return; // Already connected
    }

    // Get the WebSocket URL from environment or use default
    // Use NEXT_PUBLIC_WEBSOCKET_URL from environment variables if available
    let wsBaseUrl = process.env.NEXT_PUBLIC_WEBSOCKET_URL || '';

    // If no environment variable is set, construct from current location
    if (!wsBaseUrl) {
      const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      wsBaseUrl = `${wsProtocol}//${window.location.hostname}:8080`;
    }

    // Add the WebSocket endpoint path and user ID if provided
    const wsEndpoint = userId ? `/ws?user_id=${userId}` : '/ws';
    const wsUrl = `${wsBaseUrl}${wsEndpoint}`;

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log("WebSocket connected");
        this.isConnected = true;
        this.reconnectAttempts = 0; // Reset attempts on successful connection
        this.notifyListeners("connected", {});
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log("Received WebSocket message:", data);

          // Handle different types of messages
          if (data.type === "notification") {
            this.handleNotification(data.payload);
          } else if (data.type === "task-update") {
            this.handleTaskUpdate(data.payload);
          } else {
            // Generic message handling
            this.notifyListeners("message", data);
          }
        } catch (error) {
          console.error("Error parsing WebSocket message:", error);
          this.notifyListeners("error", { message: "Error parsing message", error });
        }
      };

      this.ws.onclose = () => {
        console.log("WebSocket disconnected");
        this.isConnected = false;
        this.notifyListeners("disconnected", {});

        // Attempt to reconnect if we haven't exceeded max attempts
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
          setTimeout(() => {
            this.connect(userId);
          }, this.reconnectInterval);
        } else {
          toast.error("Could not reconnect to real-time service. Please refresh the page.");
        }
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        this.notifyListeners("error", { message: "WebSocket error occurred", error });
      };
    } catch (error) {
      console.error("Failed to create WebSocket connection:", error);
      this.notifyListeners("error", { message: "Failed to create WebSocket connection", error });
    }
  }

  private handleNotification(payload: any) {
    // Display notification using toast
    const { title, message, type = "info", user_id } = payload;

    // Only show notification if it's for the current user or is a general notification
    if (!user_id || user_id === localStorage.getItem("current_user_id")) {
      switch (type) {
        case "success":
          toast.success(title || "Success", {
            description: message,
          });
          break;
        case "error":
          toast.error(title || "Error", {
            description: message,
          });
          break;
        case "warning":
          toast.warning(title || "Warning", {
            description: message,
          });
          break;
        default:
          toast.info(title || "Notification", {
            description: message,
          });
      }

      // Also notify listeners
      this.notifyListeners("notification", payload);
    }
  }

  private handleTaskUpdate(payload: any) {
    // Display task update notification using toast
    const { task, action, user_id } = payload;

    // Only show notification if it's for the current user or is a general notification
    if (!user_id || user_id === localStorage.getItem("current_user_id")) {
      const title = `Task ${action}`;
      const message = `Task "${task.title}" has been ${action}.`;

      toast.info(title, {
        description: message,
      });

      // Also notify listeners
      this.notifyListeners("task-update", payload);
    }
  }

  public disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
      this.isConnected = false;
    }
  }

  public subscribe(eventType: string, callback: Function) {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, []);
    }
    this.listeners.get(eventType)?.push(callback);
  }

  public unsubscribe(eventType: string, callback: Function) {
    if (this.listeners.has(eventType)) {
      const callbacks = this.listeners.get(eventType) || [];
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  private notifyListeners(eventType: string, data: any) {
    const callbacks = this.listeners.get(eventType) || [];
    callbacks.forEach(callback => {
      try {
        callback(data);
      } catch (error) {
        console.error(`Error in ${eventType} listener:`, error);
      }
    });
  }

  public send(data: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.error("WebSocket is not connected. Cannot send data.");
      toast.error("Not connected to real-time service. Please refresh the page.");
    }
  }

  public isConnectedToWebSocket(): boolean {
    return this.isConnected && this.ws?.readyState === WebSocket.OPEN;
  }
}

export default WebSocketService.getInstance();