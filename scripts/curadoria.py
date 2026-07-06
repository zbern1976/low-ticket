#!/usr/bin/env python3
"""Curadoria do Guia Completo de Exercícios.

Cruza o dataset hasaneyldrm/exercises-dataset (taxonomia) com o
yuhonas/free-exercise-db (dados + imagens em domínio público), seleciona os
exercícios curados abaixo, copia as fotos para assets/images/ e gera
content/exercicios.json com os campos em PT-BR (instruções traduzidas em
etapa posterior).

Uso:
    python3 scripts/curadoria.py [caminho-free-exercise-db]
"""
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote_plus

REPO = Path(__file__).resolve().parent.parent
FED = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "/tmp/claude-0/-home-user-zbern1976/b46d55bf-2b00-5e49-a2f1-5e66cd723682/scratchpad/free-exercise-db"
)

# ---------------------------------------------------------------------------
# Seções do guia (ordem de publicação)
# ---------------------------------------------------------------------------
SECOES = {
    "peito": "Peito",
    "costas": "Costas",
    "ombros": "Ombros",
    "biceps": "Bíceps",
    "triceps": "Tríceps",
    "antebraco": "Antebraço e Pegada",
    "abdomen": "Abdômen e Core",
    "quadriceps": "Pernas — Quadríceps e Glúteos (ênfase frontal)",
    "posteriores": "Pernas — Posteriores e Glúteos",
    "panturrilha": "Panturrilha",
    "cardio": "Cardio e Corpo Inteiro",
    "pescoco": "Pescoço",
}

# ---------------------------------------------------------------------------
# Curadoria: nome exato no free-exercise-db -> (nome PT-BR, seção)
# ---------------------------------------------------------------------------
CURADORIA = {
    # ------------------------------ PEITO ------------------------------
    "Pushups": ("Flexão de Braço", "peito"),
    "Push-Up Wide": ("Flexão com Pegada Aberta", "peito"),
    "Incline Push-Up": ("Flexão Inclinada (mãos elevadas)", "peito"),
    "Decline Push-Up": ("Flexão Declinada (pés elevados)", "peito"),
    "Dips - Chest Version": ("Mergulho nas Paralelas (ênfase no peito)", "peito"),
    "Barbell Bench Press - Medium Grip": ("Supino Reto com Barra", "peito"),
    "Barbell Incline Bench Press - Medium Grip": ("Supino Inclinado com Barra", "peito"),
    "Decline Barbell Bench Press": ("Supino Declinado com Barra", "peito"),
    "Dumbbell Bench Press": ("Supino Reto com Halteres", "peito"),
    "Incline Dumbbell Press": ("Supino Inclinado com Halteres", "peito"),
    "Decline Dumbbell Bench Press": ("Supino Declinado com Halteres", "peito"),
    "Dumbbell Flyes": ("Crucifixo Reto com Halteres", "peito"),
    "Incline Dumbbell Flyes": ("Crucifixo Inclinado com Halteres", "peito"),
    "Butterfly": ("Voador na Máquina (Peck Deck)", "peito"),
    "Cable Crossover": ("Crucifixo no Cross Over", "peito"),
    "Machine Bench Press": ("Supino na Máquina", "peito"),
    "Straight-Arm Dumbbell Pullover": ("Pullover com Halter", "peito"),
    # ------------------------------ COSTAS ------------------------------
    "Pullups": ("Barra Fixa (pegada pronada)", "costas"),
    "Chin-Up": ("Barra Fixa Supinada (chin-up)", "costas"),
    "Wide-Grip Lat Pulldown": ("Puxada Alta com Pegada Aberta", "costas"),
    "Close-Grip Front Lat Pulldown": ("Puxada Alta com Pegada Fechada", "costas"),
    "V-Bar Pulldown": ("Puxada com Triângulo", "costas"),
    "Straight-Arm Pulldown": ("Pulldown com Braços Estendidos", "costas"),
    "Bent Over Barbell Row": ("Remada Curvada com Barra", "costas"),
    "One-Arm Dumbbell Row": ("Remada Unilateral com Halter (serrote)", "costas"),
    "Bent Over Two-Dumbbell Row": ("Remada Curvada com Halteres", "costas"),
    "Seated Cable Rows": ("Remada Baixa Sentada (cabo)", "costas"),
    "Inverted Row": ("Remada Invertida (peso corporal)", "costas"),
    "T-Bar Row with Handle": ("Remada Cavalinho (barra T)", "costas"),
    "Leverage Iso Row": ("Remada Articulada na Máquina", "costas"),
    "Barbell Deadlift": ("Levantamento Terra com Barra", "costas"),
    "Rack Pulls": ("Levantamento Terra Parcial (rack pull)", "costas"),
    "Hyperextensions (Back Extensions)": ("Extensão Lombar (banco romano)", "costas"),
    "Barbell Shrug": ("Encolhimento de Ombros com Barra", "costas"),
    "Dumbbell Shrug": ("Encolhimento de Ombros com Halteres", "costas"),
    # ------------------------------ OMBROS ------------------------------
    "Standing Military Press": ("Desenvolvimento Militar em Pé", "ombros"),
    "Seated Barbell Military Press": ("Desenvolvimento com Barra Sentado", "ombros"),
    "Dumbbell Shoulder Press": ("Desenvolvimento com Halteres", "ombros"),
    "Seated Dumbbell Press": ("Desenvolvimento com Halteres Sentado", "ombros"),
    "Arnold Dumbbell Press": ("Desenvolvimento Arnold", "ombros"),
    "Standing Dumbbell Press": ("Desenvolvimento com Halteres em Pé", "ombros"),
    "Side Lateral Raise": ("Elevação Lateral", "ombros"),
    "Front Dumbbell Raise": ("Elevação Frontal com Halteres", "ombros"),
    "Reverse Flyes": ("Crucifixo Invertido com Halteres", "ombros"),
    "Face Pull": ("Face Pull (puxada para o rosto)", "ombros"),
    "Upright Barbell Row": ("Remada Alta com Barra", "ombros"),
    "Machine Shoulder (Military) Press": ("Desenvolvimento na Máquina", "ombros"),
    "Cable Seated Lateral Raise": ("Elevação Lateral no Cabo (sentado)", "ombros"),
    "Push Press": ("Desenvolvimento com Impulso (push press)", "ombros"),
    # ------------------------------ BÍCEPS ------------------------------
    "Barbell Curl": ("Rosca Direta com Barra", "biceps"),
    "EZ-Bar Curl": ("Rosca Direta com Barra W", "biceps"),
    "Dumbbell Bicep Curl": ("Rosca Direta com Halteres", "biceps"),
    "Dumbbell Alternate Bicep Curl": ("Rosca Alternada com Halteres", "biceps"),
    "Hammer Curls": ("Rosca Martelo", "biceps"),
    "Concentration Curls": ("Rosca Concentrada", "biceps"),
    "Incline Dumbbell Curl": ("Rosca Inclinada com Halteres", "biceps"),
    "Preacher Curl": ("Rosca Scott (banco preacher)", "biceps"),
    "Machine Bicep Curl": ("Rosca na Máquina", "biceps"),
    "Standing Biceps Cable Curl": ("Rosca no Cabo em Pé", "biceps"),
    "Cable Hammer Curls - Rope Attachment": ("Rosca Martelo no Cabo (corda)", "biceps"),
    "Zottman Curl": ("Rosca Zottman", "biceps"),
    # ------------------------------ TRÍCEPS ------------------------------
    "Dips - Triceps Version": ("Mergulho nas Paralelas (ênfase no tríceps)", "triceps"),
    "Bench Dips": ("Mergulho no Banco", "triceps"),
    "Close-Grip Barbell Bench Press": ("Supino com Pegada Fechada", "triceps"),
    "EZ-Bar Skullcrusher": ("Tríceps Testa com Barra W", "triceps"),
    "Lying Dumbbell Tricep Extension": ("Tríceps Testa com Halteres", "triceps"),
    "Standing Dumbbell Triceps Extension": ("Tríceps Francês com Halter", "triceps"),
    "Tricep Dumbbell Kickback": ("Tríceps Coice com Halter", "triceps"),
    "Triceps Pushdown": ("Tríceps na Polia (barra reta)", "triceps"),
    "Triceps Pushdown - Rope Attachment": ("Tríceps na Polia com Corda", "triceps"),
    "Cable Rope Overhead Triceps Extension": ("Tríceps Francês no Cabo (corda)", "triceps"),
    "Push-Ups - Close Triceps Position": ("Flexão com Pegada Fechada (diamante)", "triceps"),
    "Machine Triceps Extension": ("Tríceps na Máquina", "triceps"),
    # ------------------------------ ANTEBRAÇO ------------------------------
    "Palms-Up Barbell Wrist Curl Over A Bench": ("Rosca de Punho com Barra (palmas para cima)", "antebraco"),
    "Palms-Down Wrist Curl Over A Bench": ("Rosca de Punho Invertida (palmas para baixo)", "antebraco"),
    "Seated Dumbbell Palms-Up Wrist Curl": ("Rosca de Punho com Halter", "antebraco"),
    "Farmer's Walk": ("Caminhada do Fazendeiro", "antebraco"),
    "Wrist Roller": ("Rolo de Punho", "antebraco"),
    "Plate Pinch": ("Pinça de Anilhas", "antebraco"),
    # ------------------------------ ABDÔMEN ------------------------------
    "Crunches": ("Abdominal Crunch", "abdomen"),
    "Sit-Up": ("Abdominal Completo (sit-up)", "abdomen"),
    "3/4 Sit-Up": ("Abdominal 3/4", "abdomen"),
    "Plank": ("Prancha", "abdomen"),
    "Side Bridge": ("Prancha Lateral", "abdomen"),
    "Reverse Crunch": ("Abdominal Invertido", "abdomen"),
    "Russian Twist": ("Rotação Russa (russian twist)", "abdomen"),
    "Flat Bench Lying Leg Raise": ("Elevação de Pernas no Banco", "abdomen"),
    "Hanging Leg Raise": ("Elevação de Pernas na Barra", "abdomen"),
    "Cable Crunch": ("Abdominal no Cabo (ajoelhado)", "abdomen"),
    "Ab Roller": ("Roda Abdominal", "abdomen"),
    "Dead Bug": ("Dead Bug (inseto morto)", "abdomen"),
    "Cross-Body Crunch": ("Abdominal Cruzado (oblíquo)", "abdomen"),
    "Oblique Crunches": ("Abdominal Oblíquo", "abdomen"),
    "Exercise Ball Crunch": ("Abdominal na Bola Suíça", "abdomen"),
    "Pallof Press": ("Pallof Press (anti-rotação)", "abdomen"),
    "Decline Crunch": ("Abdominal no Banco Declinado", "abdomen"),
    # ------------------------------ QUADRÍCEPS ------------------------------
    "Barbell Squat": ("Agachamento Livre com Barra", "quadriceps"),
    "Barbell Full Squat": ("Agachamento Profundo com Barra", "quadriceps"),
    "Front Barbell Squat": ("Agachamento Frontal com Barra", "quadriceps"),
    "Bodyweight Squat": ("Agachamento Livre (peso corporal)", "quadriceps"),
    "Dumbbell Squat": ("Agachamento com Halteres", "quadriceps"),
    "Goblet Squat": ("Agachamento Goblet", "quadriceps"),
    "Plie Dumbbell Squat": ("Agachamento Sumô com Halter", "quadriceps"),
    "Barbell Lunge": ("Afundo com Barra", "quadriceps"),
    "Dumbbell Lunges": ("Afundo com Halteres", "quadriceps"),
    "Bodyweight Walking Lunge": ("Passada (avanço caminhando)", "quadriceps"),
    "Dumbbell Step Ups": ("Subida no Banco com Halteres", "quadriceps"),
    "Leg Press": ("Leg Press", "quadriceps"),
    "Leg Extensions": ("Cadeira Extensora", "quadriceps"),
    "Hack Squat": ("Agachamento no Hack", "quadriceps"),
    "Smith Machine Squat": ("Agachamento no Smith", "quadriceps"),
    "Freehand Jump Squat": ("Agachamento com Salto", "quadriceps"),
    "Split Squat with Dumbbells": ("Agachamento Búlgaro com Halteres", "quadriceps"),
    # ------------------------------ POSTERIORES ------------------------------
    "Romanian Deadlift": ("Levantamento Terra Romeno", "posteriores"),
    "Stiff-Legged Barbell Deadlift": ("Stiff com Barra", "posteriores"),
    "Stiff-Legged Dumbbell Deadlift": ("Stiff com Halteres", "posteriores"),
    "Sumo Deadlift": ("Levantamento Terra Sumô", "posteriores"),
    "Good Morning": ("Bom Dia (good morning)", "posteriores"),
    "Lying Leg Curls": ("Mesa Flexora", "posteriores"),
    "Seated Leg Curl": ("Cadeira Flexora", "posteriores"),
    "Standing Leg Curl": ("Flexora em Pé", "posteriores"),
    "Barbell Hip Thrust": ("Elevação Pélvica com Barra (hip thrust)", "posteriores"),
    "Barbell Glute Bridge": ("Ponte de Glúteos com Barra", "posteriores"),
    "Butt Lift (Bridge)": ("Ponte de Glúteos (peso corporal)", "posteriores"),
    "Single Leg Glute Bridge": ("Ponte de Glúteos Unilateral", "posteriores"),
    "Glute Kickback": ("Coice de Glúteos (quatro apoios)", "posteriores"),
    "One-Legged Cable Kickback": ("Coice de Glúteos no Cabo", "posteriores"),
    "Pull Through": ("Pull Through no Cabo", "posteriores"),
    "Step-up with Knee Raise": ("Subida no Banco com Elevação de Joelho", "posteriores"),
    # ------------------------------ PANTURRILHA ------------------------------
    "Standing Calf Raises": ("Panturrilha em Pé na Máquina", "panturrilha"),
    "Seated Calf Raise": ("Panturrilha Sentado na Máquina", "panturrilha"),
    "Calf Press On The Leg Press Machine": ("Panturrilha no Leg Press", "panturrilha"),
    "Standing Dumbbell Calf Raise": ("Panturrilha em Pé com Halteres", "panturrilha"),
    "Standing Barbell Calf Raise": ("Panturrilha em Pé com Barra", "panturrilha"),
    "Barbell Seated Calf Raise": ("Panturrilha Sentado com Barra", "panturrilha"),
    "Smith Machine Calf Raise": ("Panturrilha no Smith", "panturrilha"),
    "Donkey Calf Raises": ("Panturrilha Burrinho", "panturrilha"),
    # ------------------------------ CARDIO ------------------------------
    "Rope Jumping": ("Pular Corda", "cardio"),
    "Running, Treadmill": ("Corrida na Esteira", "cardio"),
    "Bicycling, Stationary": ("Bicicleta Ergométrica", "cardio"),
    "Elliptical Trainer": ("Elíptico", "cardio"),
    "Rowing, Stationary": ("Remo Ergômetro", "cardio"),
    "Mountain Climbers": ("Escalador (mountain climber)", "cardio"),
    "Star Jump": ("Polichinelo com Salto (star jump)", "cardio"),
    "Air Bike": ("Abdominal Bicicleta (air bike)", "cardio"),
    "Front Box Jump": ("Salto na Caixa", "cardio"),
    "One-Arm Kettlebell Swings": ("Kettlebell Swing Unilateral", "cardio"),
    "Sled Push": ("Empurrar Trenó (sled push)", "cardio"),
    "Battling Ropes": ("Cordas Navais (battle rope)", "cardio"),
    "Kettlebell Thruster": ("Thruster com Kettlebell", "cardio"),
    "Burpee": ("Burpee", "cardio"),  # pode não existir na base; validado abaixo
    # ------------------------------ PESCOÇO ------------------------------
    "Isometric Neck Exercise - Front And Back": ("Isometria de Pescoço (frente e trás)", "pescoco"),
    "Isometric Neck Exercise - Sides": ("Isometria de Pescoço (lateral)", "pescoco"),
}

MUSCULOS_PT = {
    "abdominals": "Abdômen", "abductors": "Abdutores", "adductors": "Adutores",
    "biceps": "Bíceps", "calves": "Panturrilhas", "chest": "Peitoral",
    "forearms": "Antebraços", "glutes": "Glúteos", "hamstrings": "Posteriores de coxa",
    "lats": "Dorsais", "lower back": "Lombar", "middle back": "Meio das costas",
    "neck": "Pescoço", "quadriceps": "Quadríceps", "shoulders": "Ombros",
    "traps": "Trapézio", "triceps": "Tríceps",
}
EQUIP_PT = {
    "barbell": "Barra", "dumbbell": "Halteres", "body only": "Peso corporal",
    "cable": "Cabo/Polia", "machine": "Máquina", "kettlebells": "Kettlebell",
    "bands": "Elástico", "medicine ball": "Medicine ball", "exercise ball": "Bola suíça",
    "e-z curl bar": "Barra W", "foam roll": "Rolo de espuma", "other": "Acessórios",
    None: "Sem equipamento",
}
NIVEL_PT = {"beginner": "Iniciante", "intermediate": "Intermediário", "expert": "Avançado"}
FORCA_PT = {"push": "Empurrar", "pull": "Puxar", "static": "Estático", None: "—"}
MECANICA_PT = {"compound": "Composto", "isolation": "Isolado", None: "—"}


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return s


def main():
    fed = {d["name"]: d for d in json.loads((FED / "dist/exercises.json").read_text())}

    faltando = [n for n in CURADORIA if n not in fed]
    if faltando:
        print(f"AVISO: {len(faltando)} nomes não encontrados na base (serão pulados):")
        for n in faltando:
            print("  -", n)

    img_dir = REPO / "assets/images"
    img_dir.mkdir(parents=True, exist_ok=True)
    (REPO / "content").mkdir(exist_ok=True)

    exercicios = []
    ordem_secao = {k: i for i, k in enumerate(SECOES)}
    for en_name, (pt_name, secao) in CURADORIA.items():
        if en_name not in fed:
            continue
        d = fed[en_name]
        if not d.get("images"):
            print(f"AVISO: sem imagens, pulando: {en_name}")
            continue
        slug = slugify(pt_name)
        imagens = []
        for i, rel in enumerate(d["images"][:2]):
            src = FED / "exercises" / rel
            dst = img_dir / f"{slug}-{i}.jpg"
            shutil.copyfile(src, dst)
            imagens.append(f"assets/images/{dst.name}")
        busca = "como fazer " + re.sub(r"\s*\(.*?\)", "", pt_name).strip() + " exercício"
        video_url = "https://www.youtube.com/results?search_query=" + quote_plus(busca)
        exercicios.append({
            "id": slug,
            "nome": pt_name,
            "nome_original": en_name,
            "grupo": secao,
            "grupo_titulo": SECOES[secao],
            "musculo_alvo": MUSCULOS_PT.get(d["primaryMuscles"][0] if d["primaryMuscles"] else "", "—"),
            "musculos_secundarios": [MUSCULOS_PT.get(m, m) for m in d.get("secondaryMuscles", [])],
            "equipamento": EQUIP_PT.get(d.get("equipment"), d.get("equipment") or "—"),
            "nivel": NIVEL_PT.get(d.get("level"), "—"),
            "forca": FORCA_PT.get(d.get("force"), "—"),
            "mecanica": MECANICA_PT.get(d.get("mechanic"), "—"),
            "imagens": imagens,
            "qrcode": f"assets/qrcodes/{slug}.png",
            "video_url": video_url,
            "instrucoes_en": d.get("instructions", []),
            "instrucoes": [],
        })

    exercicios.sort(key=lambda e: (ordem_secao[e["grupo"]], e["nome"]))
    out = REPO / "content/exercicios.json"
    out.write_text(json.dumps(exercicios, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nOK: {len(exercicios)} exercícios curados -> {out}")
    from collections import Counter
    for g, c in Counter(e["grupo"] for e in exercicios).items():
        print(f"  {SECOES[g]}: {c}")


if __name__ == "__main__":
    main()
