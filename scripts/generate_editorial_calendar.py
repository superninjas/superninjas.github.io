import json
from datetime import datetime, timedelta
import calendar

def generate_calendar(ideas_file, output_file):
    with open(ideas_file, 'r', encoding='utf-8') as f:
        ideas = json.load(f)

    total_articles = len(ideas)
    if total_articles == 0:
        print("Nenhuma ideia de conteúdo encontrada para gerar o calendário.")
        return

    start_date = datetime(2026, 7, 1) # Start from July 1st, 2026
    
    calendar_plan = []
    current_date = start_date
    article_index = 0

    while article_index < total_articles:
        # Skip weekends
        if current_date.weekday() >= 5: # 5 is Saturday, 6 is Sunday
            current_date += timedelta(days=1)
            continue

        # Assign articles for the current day until all are assigned or day ends
        while article_index < total_articles and current_date.weekday() < 5: # Still a weekday
            idea = ideas[article_index]
            month_name = calendar.month_name[current_date.month]
            year = current_date.year
            
            calendar_plan.append({
                "data_publicacao": current_date.strftime("%Y-%m-%d"),
                "mes": f"{month_name} {year}",
                "categoria": idea["categoria"],
                "tipo_conteudo": idea["tipo_conteudo"],
                "titulo": idea["titulo"],
                "palavra_chave_alvo": idea["palavra_chave_alvo"],
                "volume_estimado": idea["volume_estimado"],
                "dificuldade_estimada": idea["dificuldade_estimada"]
            })
            article_index += 1
            
            # To distribute articles more evenly, we can assign a few per day
            # For 400 articles over ~260 weekdays, that's roughly 1.5 articles/day.
            # Let's assign 1 or 2 articles per weekday.
            if article_index % 2 == 0 and article_index < total_articles:
                # Assign another article to the same day if available
                if current_date.weekday() < 5: # Ensure it's still a weekday
                    idea = ideas[article_index]
                    calendar_plan.append({
                        "data_publicacao": current_date.strftime("%Y-%m-%d"),
                        "mes": f"{month_name} {year}",
                        "categoria": idea["categoria"],
                        "tipo_conteudo": idea["tipo_conteudo"],
                        "titulo": idea["titulo"],
                        "palavra_chave_alvo": idea["palavra_chave_alvo"],
                        "volume_estimado": idea["volume_estimado"],
                        "dificuldade_estimada": idea["dificuldade_estimada"]
                    })
                    article_index += 1

        current_date += timedelta(days=1)

    # Group by month for the report
    monthly_plan = {}
    for item in calendar_plan:
        month = item["mes"]
        if month not in monthly_plan:
            monthly_plan[month] = []
        monthly_plan[month].append(item)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(monthly_plan, f, indent=2, ensure_ascii=False)
        
    print(f"Calendário editorial gerado em {output_file} com {len(calendar_plan)} artigos.")

if __name__ == "__main__":
    generate_calendar('content_ideas.json', 'calendario_editorial.json')
