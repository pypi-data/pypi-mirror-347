class Course:

    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self):
        return f"{self.name} [{self.duration} horas] ({self.link})"

course_list = [
    Course("Introducción a Linux", 15,"https://hack4u.io/cursos/introduccion-a-linux/"),
    Course("Personalización de Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
    Course("Introducción al Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/")
]

def list_courses():
    for course in course_list:
        print(course)

def search_course_by_name(name):
    for course in course_list:
        if course.name == name:
            return course
        
    return None
