import socket
import random
import csv


def trimite_numar(port , fisier):
    try:
        numar = (random.randint(0, 2))
        
        with open(fisier , mode=’a’, newline=’’) as f:
            scriere = csv.writer(f)
            scriere.writerow([numar])
            
        port.sendall(str(numar).encode())
        print("S-a trimis la ESP numarul: ", numar)

        except Exception as e:
        print("Eroare trimitere date:", e)
        
        
def main():
    esp_ip = '172.20.10.13'
    esp_port = 80
    esp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    esp_socket.connect((esp_ip, esp_port))

    file_path = "C:/Users/Adda/PycharmProjects/licenta/comanda_esp.csv"
    
    try:
        trimite_numar(esp_socket, file_path)

    except Exception as e:
        print("Eroare:", e)
    finally:
        esp_socket.close()
        

if __name__ == "__main__":
    main()
