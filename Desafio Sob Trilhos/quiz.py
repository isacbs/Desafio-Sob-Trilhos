import pygame
import sys
import os
from ranking import ranking

class Quiz:
    def __init__(self, player_name, tempo_total):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Quiz de Cidadania Urbana")
        
        self.player_name = player_name
        self.tempo_total = tempo_total
        self.BASE_DIR = os.path.dirname(__file__)
        self.IMG_DIR = os.path.join(self.BASE_DIR, "imgs")
        
        # Configurações de fonte e cores
        self.font = pygame.font.SysFont("Arial", 30)
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.AMARELO = (253, 214, 3)
        self.BRANCO = (255, 255, 255)
        self.VERDE = (0, 255, 0)
        self.VERMELHO = (255, 0, 0)
        
        # Perguntas do quiz
        self.questions = [
            {
                "question": "O QUE VOCÊ DEVE FAZER AO ESCUTAR O AVISO DE FECHAMENTO DAS PORTAS?",
                "options": [
                    "A) Tentar segurar a porta com o braço",
                    "B) Esperar o próximo trem com segurança",
                    "C) Pedir para o maquinista abrir novamente",
                    "D) Reclamar com os seguranças"
                ],
                "correct": "B",
                "image": "quizum.png"
            },
            {
                "question": "O USO DE ESCADAS ROLANTES DEVE RESPEITAR QUAL DESSAS REGRAS?",
                "options": [
                    "A) Ficar parado de qualquer lado",
                    "B) Sentar nos degraus",
                    "C) Deixar o lado esquerdo livre",
                    "D) Usar só quando estiver com preguiça"
                ],
                "correct": "C",
                "image": "quizdois.png"
            },
            {
                "question": "QUAL ATITUDE AJUDA A MANTER O METRÔ LIMPO?",
                "options": [
                    "A) Comer e depois limpar",
                    "B) Jogar lixo no chão só se for papel",
                    "C) Guardar seu lixo até encontrar uma lixeira",
                    "D) Deixar o lixo em cima do banco"
                ],
                "correct": "C",
                "image": "quiztres.png"
            }
        ]
        
        self.current_question = 0
        self.score = 0

    def load_image(self, image_name):
        """Carrega uma imagem com tratamento de erro"""
        try:
            image = pygame.image.load(os.path.join(self.IMG_DIR, image_name)).convert()
            return pygame.transform.scale(image, (800, 600))
        except:
            print(f"Erro ao carregar imagem: {image_name}")
            surface = pygame.Surface((800, 600))
            surface.fill((0, 0, 0))
            return surface

    def show_question(self):
        """Mostra a pergunta atual na tela"""
        question = self.questions[self.current_question]
        background = self.load_image(question["image"])
        
        self.screen.blit(background, (0, 0))
        
        # Se a imagem não carregou (tela preta), mostra a pergunta como texto
        if background.get_at((0, 0)) == (0, 0, 0):
            title = self.title_font.render(question["question"], True, self.BRANCO)
            self.screen.blit(title, (50, 50))
            
            for i, option in enumerate(question["options"]):
                text = self.font.render(option, True, self.BRANCO)
                self.screen.blit(text, (50, 150 + i * 50))
        
        pygame.display.flip()

    def check_answer(self, answer):
        """Verifica se a resposta está correta"""
        correct = self.questions[self.current_question]["correct"]
        if answer == correct:
            self.score += 1
            return True
        return False

    def show_feedback(self, is_correct):
        """Mostra feedback visual da resposta"""
        if is_correct:
            text = "Resposta Correta!"
            color = self.VERDE
        else:
            correct_answer = self.questions[self.current_question]["correct"]
            text = f"Incorreto! A resposta correta era {correct_answer}"
            color = self.VERMELHO
        
        feedback = self.font.render(text, True, color)
        self.screen.blit(feedback, (400 - feedback.get_width() // 2, 500))
        pygame.display.flip()
        pygame.time.delay(1500)

    def show_result(self):
        """Mostra o resultado final do quiz"""
        self.screen.fill((0, 0, 0))
        result_text = self.title_font.render(
            f"Você acertou {self.score} de {len(self.questions)} perguntas!", 
            True, self.AMARELO)
        
        continue_text = self.font.render(
            "Pressione qualquer tecla para continuar...", 
            True, self.BRANCO)
        
        self.screen.blit(result_text, (400 - result_text.get_width() // 2, 250))
        self.screen.blit(continue_text, (400 - continue_text.get_width() // 2, 350))
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

    def run(self):
        """Executa o fluxo principal do quiz"""
        for self.current_question in range(len(self.questions)):
            self.show_question()
            
            waiting_for_answer = True
            while waiting_for_answer:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            correct = self.check_answer("A")
                            self.show_feedback(correct)
                            waiting_for_answer = False
                        elif event.key == pygame.K_b:
                            correct = self.check_answer("B")
                            self.show_feedback(correct)
                            waiting_for_answer = False
                        elif event.key == pygame.K_c:
                            correct = self.check_answer("C")
                            self.show_feedback(correct)
                            waiting_for_answer = False
                        elif event.key == pygame.K_d:
                            correct = self.check_answer("D")
                            self.show_feedback(correct)
                            waiting_for_answer = False
        
        self.show_result()
        # Redireciona para o ranking exatamente como no código original
        return ranking(self.player_name, self.tempo_total)

def run_quiz(player_name, tempo_total):
    """Função para iniciar o quiz"""
    quiz = Quiz(player_name, tempo_total)
    return quiz.run()

if __name__ == "__main__":
    # Modo de teste
    run_quiz("Jogador Teste", 0)
