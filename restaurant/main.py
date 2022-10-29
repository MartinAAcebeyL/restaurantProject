import random

def read_txt(str):
    datos = []
    with open(str) as fname:
        lineas = fname.readlines()
        for linea in lineas:
            datos.append(linea.strip('\n'))
    return datos

SOPAS = read_txt('sopas.txt')
SEGUNDOS = read_txt('segundos.txt')
DIAS = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']
NUMERO_2DOS = 2

menu_semana = {
    'lunes':{
        'sopa':'',
        'segundos':[]
    },
    'martes':{
        'sopa':'',
        'segundos':[]
    },
    'miercoles':{
        'sopa':'',
        'segundos':[]
    },
    'jueves':{
        'sopa':'',
        'segundos':[]
    },
    'viernes':{
        'sopa':'',
        'segundos':[]
    }
}

def create_menu(sopas = SOPAS, segundos = SEGUNDOS, dias = DIAS):
    global menu_semana
    for dia in dias:
        ale_sopas = random.randint(0, len(sopas)-1)
        menu_semana[dia]['sopa']=sopas.pop(ale_sopas)
        for i in range(NUMERO_2DOS):
            ale_segundos = random.randint(0, len(segundos)-1)
            menu_semana[dia]['segundos'].append(segundos.pop(ale_segundos))

def view_menu():
    global menu_semana
    for dia in DIAS:
        print('********')
        print(f'dia {dia}')
        print(f'sopa {menu_semana[dia]["sopa"]}')
        for i in range(NUMERO_2DOS):
            print(f'segundos {menu_semana[dia]["segundos"][i]}')


if __name__ == '__main__':
    create_menu()
    view_menu()