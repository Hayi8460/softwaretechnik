import pygame
import random
import sys
import time

# Grundlegende Initialisierung
pygame.init()
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maulwurf-Herausforderung")

# Farbcodes
COLORS = {
    "bg": (210, 220, 230),         # Hintergrund
    "mole": (105, 58, 47),         # Maulwurf
    "text": (0, 0, 0),             # Standard-Text
    "time": (90, 90, 90),          # Zeit-Abgelaufen-Text
    "button": (0, 123, 255),       # Button normal
    "hover": (0, 100, 200),        # Button Hover
    "btn_text": (255, 255, 255)    # Button-Schrift
}

# Schriftarten und Größen
FONT = {
    "title": pygame.font.SysFont("Segoe UI", 36, bold=True),
    "main": pygame.font.SysFont("Segoe UI", 28, bold=True),
    "small": pygame.font.SysFont("Segoe UI", 22)
}

clock = pygame.time.Clock()
mole_radius = 30  # Radius für den Maulwurf-Kreis

# Gibt zufällige neue Position für den Maulwurf zurück (mit Puffer zu Rand)
def get_new_position():
    return (
        random.randint(mole_radius, WIDTH - mole_radius),
        random.randint(mole_radius + 60, HEIGHT - mole_radius)
    )

# Zeichnet einen runden Button mit Text (inkl. Hover-Effekt)
def draw_button(rect, text, hovered):
    color = COLORS["hover"] if hovered else COLORS["button"]
    pygame.draw.rect(window, color, rect, border_radius=8)
    label = FONT["small"].render(text, True, COLORS["btn_text"])
    window.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

# Startbildschirm anzeigen (Titel, Hinweis, Startbutton)
def show_start_screen():
    while True:
        window.fill(COLORS["bg"])
        title = FONT["title"].render("Maulwurf-Herausforderung", True, COLORS["text"])
        hint = FONT["small"].render("Klicke, um das Spiel zu starten.", True, COLORS["text"])
        button = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 + 50, 220, 60)

        window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        window.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 100))

        mouse_pos = pygame.mouse.get_pos()
        draw_button(button, "Spiel starten", button.collidepoint(mouse_pos))
        pygame.display.update()

        # Event-Handling für Start
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(event.pos):
                return  # Start

# Hauptspielfunktion
def game_loop():
    score = 0
    mole_pos = get_new_position()
    start_time = time.time()
    duration = 30  # Spielzeit in Sekunden

    while True:
        window.fill(COLORS["bg"])
        remaining = max(0, int(duration - (time.time() - start_time)))

        # Maulwurf anzeigen
        pygame.draw.circle(window, COLORS["mole"], mole_pos, mole_radius)

        # Punktestand oben links
        score_text = FONT["main"].render(f"Punkte: {score:02}", True, COLORS["text"])
        window.blit(score_text, (10, 10))

        # Zeit oben rechts
        time_text = FONT["main"].render(f"Zeit: {remaining:02}", True, COLORS["text"])
        window.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

        # Spielende
        if remaining <= 0:
            end_text = FONT["main"].render("Zeit abgelaufen!", True, COLORS["time"])
            window.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - 60))
            retry_btn = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 + 20, 220, 60)
            draw_button(retry_btn, "Nochmal spielen", retry_btn.collidepoint(pygame.mouse.get_pos()))
            pygame.display.update()

            # Warten auf Klick zum Neustart
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and retry_btn.collidepoint(event.pos):
                        return  # Neustart

        # Event-Handling im laufenden Spiel
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Prüfen ob auf Maulwurf geklickt wurde
                if ((event.pos[0] - mole_pos[0])**2 + (event.pos[1] - mole_pos[1])**2) ** 0.5 <= mole_radius:
                    score += 1
                    mole_pos = get_new_position()

        pygame.display.update()
        clock.tick(60)  # 60 FPS

# Spiel ausführen
while True:
    show_start_screen()   # Anzeige bis Spiel gestartet wird
    game_loop()           # Spiel läuft, danach wieder zum Startbildschirm
