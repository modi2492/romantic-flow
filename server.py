import socket
import os
import time

def start_spoofed_server():
    port = int(os.environ.get("PORT", 8080))
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('0.0.0.0', port))
    server_sock.listen(5)
    print(f"[*] Spoofed TCP Server listening on port: {port}...")

    while True:
        try:
            client_sock, client_address = server_sock.accept()
            data = client_sock.recv(1024)
            
            # بايتات وهمية تحاكي بداية اتصال آمن لواتساب (TLS Handshake / WhatsApp Traffic)
            # هذه البايتات تخدع الـ DPI ليظن أن الاتصال مصرح به
            WHATSAPP_FAKE_HEADER = b"\x16\x03\x01\x00\xba\x01\x00\x00\xb6\x03\x03" 

            print("[*] Sending Spoofed Download packets...")
            for i in range(5):
                raw_payload = f"SERVER_DATA_PACKET_{i+1}\n".encode()
                # ندمج البايتات المزيفة مع البيانات الحقيقية
                spoofed_packet = WHATSAPP_FAKE_HEADER + raw_payload
                
                client_sock.sendall(spoofed_packet)
                time.sleep(0.2) # تأخير بسيط لضمان عدم اندماج الحزم ببعضها
            
            client_sock.close()
        except Exception as e:
            print(f"[-] Error: {e}")

if __name__ == "__main__":
    start_spoofed_server()
