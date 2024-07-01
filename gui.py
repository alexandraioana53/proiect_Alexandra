import threading
import time
import pygame
import csv
import comunicare_ESP
import rec_gest


def curata_ecranul(ecran):
    ecran.fill((0, 0, 0))
    pygame.display.flip()
    
    
def afisare_mesaj(ecran, font, mesaj, durata=None):
    ecran.fill((0, 0, 0))
    text = font.render(message, True, (255, 255, 255))
    pozitie_text = text.get_rect(center=(400, 300))
    screen.blit(text, pozitie_text)
    pygame.display.flip()
    if durata:
        time.sleep(durata)
        curata_ecranul(ecran)
        
        
def runda_urmatoare_stop_start():
    asteapta = True
    while asteapta:
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:  
                asteapta = False
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                asteapta = False
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                asteapta = False
                rec_gest.opreste_camera()
                pygame.display.quit()
                pygame.quit()
                exit()
                
                
def joc(screen, font):
    mesaje = ["3", "2", "1", "START!"]
    font_mic = pygame.font.Font(None, 36)
    for rounda in range(1, 4):
        if rounda == 2 or rounda == 3:
            display_message(screen, small_font, "Apasa tasta ENTER pentru a trece la urmatoarea runda.", duration=None)
            runda_urmatoare_stop_start()

        afisare_mesaj(ecran, font, f"Runda {round_number}", durata=2)

        for mesaj in mesaje:
            if mesaj == "START!":
                afisare_mesaj(screen, font, mesaj, durata=3)
            else:
                afisare_mesaj(ecran, font, mesaj, durata=1)

            if mesaj == "3":
                esp_thread = threading.Thread(target=comunicare_ESP.main)
                esp_thread.start()

        esp_thread.join()

        if runda == 3:
            curata_ecranul(ecran)
            
            
def scor(fisier1, fisier2):
    scor1, scor2 = 0, 0

    with open(fisier1, 'r') as f1, open(fisier2, 'r') as f2:
        citire1 = csv.reader(f1)
        citire2 = csv.reader(f2)

        for r1, r2 in zip(citire1, citire2):
            if r1 and r2:
                val1 = int(r1[0])
                val2 = int(r2[0])
                if (val1 == 0 and val2 == 1) or (val1 == 2 and val2 == 0) or (val1 == 1 and val2 == 2):
                    scor1 += 1
                elif (val1 == 1 and val2 == 0) or (val1 == 0 and val2 == 2) or (val1 == 2 and val2 == 1):
                    scor2 += 1

    return scor1, scor2
    
    
def gest_rec_thread():
    rec_gest.main()
    

def main():
    replay = False
    waiting = True

    file_path1 = "C:/Users/Adda/PycharmProjects/licenta/gestul_salvat.csv"
    file_path2 = "C:/Users/Adda/PycharmProjects/licenta/comanda_esp.csv"

    gest_thread = threading.Thread(target=gest_rec_thread)
    gest_thread.start()

    while not rec_gest.initializeaza_camera:
        time.sleep(0.1)

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Joc 'Piatră, foarfecă, hârtie'")

    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    while True:
        with open(file_path1, 'w', newline='') as file1:
            writer = csv.writer(file1)

        with open(file_path2, 'w', newline='') as file2:
            writer = csv.writer(file2)

        if not replay:
            afisare_mesaj(screen, small_font, "Apasă SPACE pentru a începe jocul", duration=None)
            runda_urmatoare_stop_start()

        joc(screen, font)

        score1, score2 = scor(file_path1, file_path2)
        score_message = f"Scorul este {score1} : {score2}"
        afisare_mesaj(screen, font, score_message, duration=5)

        afisare_mesaj(screen, font, "Jocul s-a încheiat!", duration=3)

        afisare_mesaj(screen, font, "Vrei să începi un nou joc? (d/n)", duration=None)

        replay = False
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        replay = True
                        waiting = False
                    elif event.key == pygame.K_n:
                        waiting = False
                        rec_gest.release_camera()
                        pygame.display.quit()
                        pygame.quit()
                        exit()

        if not replay:
            break
   
    
    
    
if __name__ == "__main__":
    main()