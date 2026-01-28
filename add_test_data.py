"""
Скрипт для добавления тестовых данных в базу данных FastAPI Blog

Использование:
    python add_test_data.py
"""

from sqlalchemy.orm import Session
from src.database import SessionLocal, init_db
from src.models import Category, Post
from datetime import datetime, timedelta
import random


def add_test_data():
    """Добавляет тестовые категории и посты в базу данных"""
    
    print("Инициализация базы данных...")
    init_db()
    
    db = SessionLocal()
    
    try:
        # Проверка существующих данных
        existing_categories = db.query(Category).count()
        existing_posts = db.query(Post).count()
        
        print(f"Текущее состояние БД:")
        print(f"   - Категорий: {existing_categories}")
        print(f"   - Постов: {existing_posts}")
        
        if existing_categories > 0 or existing_posts > 0:
            response = input("\nВ БД уже есть данные. Продолжить? (y/n): ")
            if response.lower() != 'y':
                print("Отменено пользователем")
                return
        
        print("\nСоздание категорий...")
        
        # Создание категорий
        categories_data = [
            {"name": "Технологии", "slug": "tech"},
            {"name": "Спорт", "slug": "sport"},
            {"name": "Наука", "slug": "science"},
            {"name": "Кулинария", "slug": "cooking"},
            {"name": "Путешествия", "slug": "travel"},
            {"name": "Образование", "slug": "education"},
        ]
        
        categories = []
        for cat_data in categories_data:
            # Проверка на дубликаты
            existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
            if not existing:
                category = Category(**cat_data)
                categories.append(category)
                print(f"   Создана категория: {cat_data['name']}")
            else:
                categories.append(existing)
                print(f"   Категория уже существует: {cat_data['name']}")
        
        if categories:
            db.add_all([c for c in categories if c.id is None])
            db.commit()
            print(f"\nСохранено {len([c for c in categories if c.id is None])} новых категорий")
        
        # Обновление списка категорий из БД
        categories = db.query(Category).all()
        
        print(f"\nСоздание постов...")
        
        # Создание постов
        posts_data = [
            {
                "name": "Введение в FastAPI",
                "description": "Полное руководство по FastAPI для начинающих. Узнайте, как создавать современные веб-API.",
                "category": "tech",
                "image_url": "/static/images/fastapi.jpg"
            },
            {
                "name": "Python 3.12: Новые возможности",
                "description": "Обзор новых функций и улучшений в Python 3.12",
                "category": "tech",
                "image_url": "/static/images/python312.jpg"
            },
            {
                "name": "Чемпионат мира по футболу 2026",
                "description": "Всё, что нужно знать о предстоящем чемпионате мира",
                "category": "sport",
                "image_url": "/static/images/worldcup2026.jpg"
            },
            {
                "name": "Тренировки для начинающих",
                "description": "Эффективные упражнения для тех, кто только начинает заниматься спортом",
                "category": "sport",
                "image_url": None
            },
            {
                "name": "Квантовая физика для всех",
                "description": "Основы квантовой механики простым языком",
                "category": "science",
                "image_url": "/static/images/quantum.jpg"
            },
            {
                "name": "Искусственный интеллект в 2026",
                "description": "Последние достижения в области ИИ и машинного обучения",
                "category": "science",
                "image_url": "/static/images/ai2026.jpg"
            },
            {
                "name": "Рецепт идеальной пиццы",
                "description": "Домашняя пицца как в ресторане за 30 минут",
                "category": "cooking",
                "image_url": "/static/images/pizza.jpg"
            },
            {
                "name": "Азиатская кухня: топ-10 блюд",
                "description": "Лучшие рецепты азиатской кухни для домашнего приготовления",
                "category": "cooking",
                "image_url": "/static/images/asian-food.jpg"
            },
            {
                "name": "Путешествие по Японии",
                "description": "Гид по самым интересным местам Японии",
                "category": "travel",
                "image_url": "/static/images/japan.jpg"
            },
            {
                "name": "Бюджетное путешествие по Европе",
                "description": "Как путешествовать по Европе недорого",
                "category": "travel",
                "image_url": None
            },
            {
                "name": "Онлайн-образование в 2026",
                "description": "Лучшие платформы для онлайн-обучения",
                "category": "education",
                "image_url": "/static/images/online-edu.jpg"
            },
            {
                "name": "Как выучить программирование",
                "description": "Пошаговый план для начинающих разработчиков",
                "category": "education",
                "image_url": "/static/images/learn-coding.jpg"
            },
        ]
        
        posts = []
        created_count = 0
        
        for idx, post_data in enumerate(posts_data):
            # Найти категорию по slug
            category_slug = post_data.pop("category")
            category = next((c for c in categories if c.slug == category_slug), None)
            
            if not category:
                print(f"   Категория '{category_slug}' не найдена, пропускаем пост")
                continue
            
            # Создать пост с датой в прошлом (от 30 дней назад до сегодня)
            days_ago = random.randint(0, 30)
            created_at = datetime.utcnow() - timedelta(days=days_ago)
            
            post = Post(
                name=post_data["name"],
                description=post_data["description"],
                category_id=category.id,
                image_url=post_data["image_url"],
                created_at=created_at
            )
            
            posts.append(post)
            created_count += 1
            print(f"   Создан пост: {post_data['name']}")
        
        if posts:
            db.add_all(posts)
            db.commit()
            print(f"\nСохранено {created_count} постов")
        
        # Итоговая статистика
        print("\n" + "="*50)
        print("ТЕСТОВЫЕ ДАННЫЕ УСПЕШНО ДОБАВЛЕНЫ!")
        print("="*50)
        
        final_categories = db.query(Category).count()
        final_posts = db.query(Post).count()
        
        print(f"\nИтоговая статистика:")
        print(f"   - Всего категорий: {final_categories}")
        print(f"   - Всего постов: {final_posts}")
        
        print(f"\nСтатистика по категориям:")
        for category in categories:
            post_count = db.query(Post).filter(Post.category_id == category.id).count()
            print(f"   - {category.name}: {post_count} постов")
        
        print(f"\nТеперь вы можете начать тестирование в Postman!")
        print(f"   API: http://localhost:8000")
        print(f"   Docs: http://localhost:8000/api/docs")
        
    except Exception as e:
        print(f"\nОШИБКА: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()


def clear_database():
    """Очищает все данные из базы данных"""
    
    print("ВНИМАНИЕ: Это удалит ВСЕ данные из базы!")
    response = input("Вы уверены? (yes/no): ")
    
    if response.lower() != 'yes':
        print("Отменено")
        return
    
    db = SessionLocal()
    
    try:
        posts_deleted = db.query(Post).delete()
        categories_deleted = db.query(Category).delete()
        db.commit()
        
        print(f"\nБаза данных очищена:")
        print(f"   - Удалено постов: {posts_deleted}")
        print(f"   - Удалено категорий: {categories_deleted}")
        
    except Exception as e:
        print(f"Ошибка при очистке: {e}")
        db.rollback()
        
    finally:
        db.close()


def show_database_info():
    """Показывает информацию о текущем состоянии базы данных"""
    
    db = SessionLocal()
    
    try:
        categories = db.query(Category).all()
        posts = db.query(Post).all()
        
        print("\n" + "="*50)
        print("ИНФОРМАЦИЯ О БАЗЕ ДАННЫХ")
        print("="*50)
        
        print(f"\nКатегории (всего: {len(categories)}):")
        for cat in categories:
            post_count = db.query(Post).filter(Post.category_id == cat.id).count()
            print(f"   {cat.id}. {cat.name} ({cat.slug}) - {post_count} постов")
        
        print(f"\nПосты (всего: {len(posts)}):")
        for post in posts[:10]:  # Показываем первые 10
            print(f"   {post.id}. {post.name}")
            print(f"      Категория: {post.category.name}")
            print(f"      Дата: {post.created_at}")
            print()
        
        if len(posts) > 10:
            print(f"   ... и еще {len(posts) - 10} постов")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    print("\n" + "="*50)
    print("УПРАВЛЕНИЕ ТЕСТОВЫМИ ДАННЫМИ")
    print("="*50)
    print("\nВыберите действие:")
    print("1. Добавить тестовые данные")
    print("2. Очистить базу данных")
    print("3. Показать информацию о БД")
    print("4. Выход")
    
    choice = input("\nВаш выбор (1-4): ")
    
    if choice == "1":
        add_test_data()
    elif choice == "2":
        clear_database()
    elif choice == "3":
        show_database_info()
    elif choice == "4":
        print("До свидания!")
    else:
        print("Неверный выбор")
