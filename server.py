import socket
import os
import time

def start_xmpp_spoofed_server():
    port = int(os.environ.get("PORT", 8080))
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('0.0.0.0', port))
    server_sock.listen(5)
    print(f"[*] XMPP-Spoofed Server listening on port: {port}...")

    while True:
        try:
            client_sock, client_address = server_sock.accept()
            data = client_sock.recv(1024)
            
            # البايتات الافتتاحية الرسمية لبروتوكول اتصال شات واتساب (FunXMPP Header)
            # تتكون عادة من الحرفين WA (بايت 0x57 و 0x41) يليهما رقم الإصدار ونوع الاتصال
            WHATSAPP_XMPP_HEADER = b"WA\x01\x05\x00\x00\x00\x08"

            print("[*] Sending FunXMPP Spoofed packets...")
            for i in range(5):
                raw_payload = f"SERVER_XMPP_DATA_{i+1}\n".encode()
                # ندمج بايتات الشات الفعلي في بداية التدفق
                spoofed_packet = WHATSAPP_XMPP_HEADER + raw_payload
                
                client_sock.sendall(spoofed_packet)
                time.sleep(0.2)
            
            client_sock.close()
        except Exception as e:
            print(f"[-] Error: {e}")

if __name__ == "__main__":
    start_xmpp_spoofed_server()
