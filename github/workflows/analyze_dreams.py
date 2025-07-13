#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from datetime import datetime
import os

class DreamAnalyzer:
    def __init__(self):
        self.emotions = {
            'positivo': ['feliz', 'alegre', 'esperança', 'amor', 'paz', 'luz', 'voar', 'liberdade'],
            'nostalgico': ['passado', 'infância', 'memória', 'saudade', 'tempo', 'antigo'],
            'misterioso': ['escuro', 'sombra', 'desconhecido', 'estranho', 'mágico', 'surreal'],
            'ansioso': ['correr', 'perseguir', 'perder', 'cair', 'medo', 'pressa', 'fugir']
        }
        
        self.future_keywords = ['futuro', 'amanhã', 'próximo', 'espero', 'quero', 'desejo', 'planejo']
        self.night_keywords = ['dormir', 'sonhei', 'pesadelo', 'acordei', 'noite', 'cama']

    def analyze_dream_content(self, content):
        """Analisa o conteúdo do sonho e retorna insights"""
        content_lower = content.lower()
        
        # Detectar tipo de sonho
        dream_type = self.detect_dream_type(content_lower)
        
        # Analisar emoções
        emotions = self.analyze_emotions(content_lower)
        
        # Extrair palavras-chave
        keywords = self.extract_keywords(content_lower)
        
        # Calcular score de positividade
        positivity_score = self.calculate_positivity(content_lower)
        
        return {
            'type': dream_type,
            'emotions': emotions,
            'keywords': keywords,
            'positivity_score': positivity_score,
            'word_count': len(content.split()),
            'analysis_date': datetime.now().isoformat()
        }

    def detect_dream_type(self, content):
        """Detecta se é sonho do futuro ou noturno"""
        future_count = sum(1 for keyword in self.future_keywords if keyword in content)
        night_count = sum(1 for keyword in self.night_keywords if keyword in content)
        
        if future_count > night_count:
            return 'futuro'
        elif night_count > future_count:
            return 'noturno'
        else:
            return 'indefinido'

    def analyze_emotions(self, content):
        """Analisa as emoções presentes no sonho"""
        emotion_scores = {}
        
        for emotion, keywords in self.emotions.items():
            score = sum(1 for keyword in keywords if keyword in content)
            if score > 0:
                emotion_scores[emotion] = score
        
        return emotion_scores

    def extract_keywords(self, content):
        """Extrai palavras-chave importantes"""
        # Remove pontuação e divide em palavras
        words = re.findall(r'\b\w+\b', content)
        
        # Filtra palavras com mais de 4 caracteres
        keywords = [word for word in words if len(word) > 4]
        
        # Conta frequência
        word_freq = {}
        for word in keywords:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Retorna as 5 palavras mais frequentes
        return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]

    def calculate_positivity(self, content):
        """Calcula um score de positividade de 0 a 100"""
        positive_words = self.emotions['positivo']
        negative_indicators = ['não', 'nunca', 'impossível', 'difícil', 'problema', 'medo']
        
        positive_count = sum(1 for word in positive_words if word in content)
        negative_count = sum(1 for word in negative_indicators if word in content)
        
        total_words = len(content.split())
        
        if total_words == 0:
            return 50
        
        # Calcula score baseado na proporção de palavras positivas/negativas
        score = 50 + (positive_count * 10) - (negative_count * 5)
        
        # Limita entre 0 e 100
        return max(0, min(100, score))

    def generate_dream_report(self, dreams_data):
        """Gera relatório completo dos sonhos"""
        if not dreams_data:
            return "Nenhum sonho para analisar."
        
        total_dreams = len(dreams_data)
        
        # Análise geral
        types_count = {}
        emotions_total = {}
        avg_positivity = 0
        
        for dream in dreams_data:
            analysis = self.analyze_dream_content(dream.get('content', ''))
            
            # Conta tipos
            dream_type = analysis['type']
            types_count[dream_type] = types_count.get(dream_type, 0) + 1
            
            # Soma emoções
            for emotion, score in analysis['emotions'].items():
                emotions_total[emotion] = emotions_total.get(emotion, 0) + score
            
            # Soma positividade
            avg_positivity += analysis['positivity_score']
        
        avg_positivity = avg_positivity / total_dreams if total_dreams > 0 else 0
        
        # Gera relatório
        report = f"""
# 🌙 RELATÓRIO DE ANÁLISE DOS SONHOS

## 📊 Estatísticas Gerais
- **Total de sonhos analisados:** {total_dreams}
- **Score médio de positividade:** {avg_positivity:.1f}/100

## 🎭 Tipos de Sonhos
"""
        
        for dream_type, count in types_count.items():
            percentage = (count / total_dreams) * 100
            report += f"- **{dream_type.title()}:** {count} sonhos ({percentage:.1f}%)\n"
        
        report += "\n## 💭 Emoções Predominantes\n"
        
        for emotion, total_score in sorted(emotions_total.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{emotion.title()}:** {total_score} ocorrências\n"
        
        report += f"\n## 🔮 Análise Gerada em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}\n"
        
        return report

def main():
    """Função principal que será executada pelo GitHub Actions"""
    print("🚀 Iniciando análise dos sonhos...")
    
    analyzer = DreamAnalyzer()
    
    # Simula dados de sonhos (em um projeto real, você leria de um arquivo JSON)
    sample_dreams = [
        {
            "content": "Sonhei que estava voando sobre uma cidade do futuro com carros voadores e prédios verdes",
            "type": "futuro",
            "date": "2025-01-10"
        },
        {
            "content": "Tive um pesadelo onde estava correndo de algo escuro e não conseguia encontrar a saída",
            "type": "noturno", 
            "date": "2025-01-09"
        },
        {
            "content": "Imagino um mundo onde todos vivem em paz e harmonia, sem guerras nem fome",
            "type": "futuro",
            "date": "2025-01-08"
        }
    ]
    
    # Gera relatório
    report = analyzer.generate_dream_report(sample_dreams)
    
    # Salva relatório em arquivo
    with open('dream_analysis_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✅ Análise concluída! Relatório salvo em 'dream_analysis_report.md'")
    print("\n" + "="*50)
    print(report)
    print("="*50)

if __name__ == "__main__":
    main()
