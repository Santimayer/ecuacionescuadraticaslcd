# Importar librerias
import math
import utime
#import ds1302
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


I2C_ADDR = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
ledverde = machine.Pin(17, machine.Pin.OUT)
ledrojo = machine.Pin(19, machine.Pin.OUT)
lcd.move_to(0,0)
lcd.putstr("Esperando input")
ledrojo.value(1)
utime.sleep_ms(100)
ledrojo.value(0)
utime.sleep_ms(500)
ledverde.value(1)
utime.sleep_ms(100)
ledverde.value(0)
# Función para calcular el discriminante de la ecuación cuadrática
def calcular_discriminante(coeficiente_a, coeficiente_b, termino_independiente):
  """
  Calcula el discriminante de la ecuación cuadrática ax^2 + bx + c = 0.

  Args:
    coeficiente_a: El coeficiente del término x^2.
    coeficiente_b: El coeficiente del término x.
    termino_independiente: El término constante.

  Returns:
    El discriminante de la ecuación.
  """

  return coeficiente_b**2 - 4 * coeficiente_a * termino_independiente

# Función para convertir un número decimal a una fracción en su mínima expresión
def convertir_decimal_a_fraccion(numero_decimal):
  """
  Convierte un número decimal a una fracción en su mínima expresión.

  Args:
    numero_decimal: El número decimal a convertir.

  Returns:
    Una tupla que contiene el numerador y denominador de la fracción.
  """

  # Convertir el número decimal a una cadena
  multiplicador = 10**len(str(numero_decimal).split('.')[1])
  numerador = int(numero_decimal * multiplicador)

  # Encontrar el MCD del numerador y denominador
  mcd = _gcd(numerador, multiplicador)

  # Simplificar la fracción
  return numerador // mcd, multiplicador // mcd

def _gcd(a, b):
  """
  Calcula el máximo común divisor de dos números.

  Args:
    a: El primer número.
    b: El segundo número.

  Returns:
    El MCD de a y b.
  """

  while b:
    a, b = b, a % b
  return a

# Entrada de los valores
valor_a = int(input("Valor de a: "))
valor_b = int(input("Valor de b: "))
valor_c = int(input("Valor de c: "))

# Calcular el discriminante
discriminante = calcular_discriminante(valor_a, valor_b, valor_c)

# Mostrar el resultado dependiendo del valor del discriminante
if discriminante < 0:
  print(f"No tiene soluciones reales ya que el discriminante vale: {discriminante}")
  print(f"""
  a = {valor_a}
  b = {valor_b}
  c = {valor_c}

  Para calcular el discriminante se tiene que realizar:

  √b^2 - 4ac

  √(({valor_b})^2 - 4({valor_a})({valor_c}))

  √{discriminante} = Los numeros negativos no tienen raiz cuadrada
  """)
  lcd.clear()
  lcd.putstr("No tiene")
  lcd.move_to(0,1)
  lcd.putstr("solucion")
  ledrojo.value(1)
  utime.sleep(2)
  ledrojo.value(0)
elif discriminante == 0:
  solucion = -valor_b / (2 * valor_a)
  # Convertir la solucion a fraccion
  numerador_solucion, denominador_solucion = convertir_decimal_a_fraccion(solucion)
  print(f"Tiene una sola solucion real ya que el discriminante vale: {discriminante}")
  print(f"""
  a = {valor_a}
  b = {valor_b}
  c = {valor_c}

  Para calcular el discriminante se tiene que realizar:

  √b^2 - 4ac

  √(({valor_b})^2 - 4({valor_a})({valor_c}))

  √{discriminante} = {math.sqrt(discriminante)}
  """)
  # Imprimir la solucion
  print(f"La solución es: {numerador_solucion}/{denominador_solucion} = {solucion}")
  lcd.clear()
  lcd.putstr(f"Sol1={solucion}")
  ledverde.value(1)
  utime.sleep(2)
  ledverde.value(0)
else:
  solucion_1 = (-valor_b + math.sqrt(discriminante)) / (2 * valor_a)
  solucion_2 = (-valor_b - math.sqrt(discriminante)) / (2 * valor_a)
  # Convertir las soluciones a fracciones
  numerador_solucion_1, denominador_solucion_1 = convertir_decimal_a_fraccion(solucion_1)
  numerador_solucion_2, denominador_solucion_2 = convertir_decimal_a_fraccion(solucion_2)
  print(f"Tiene 2 soluciones reales ya que el discriminante vale: {discriminante}")
  print(f"""
  a = {valor_a}
  b = {valor_b}
  c = {valor_c}

  Para calcular el discriminante se tiene que realizar:

  √b^2 - 4ac

  √(({valor_b})^2 - 4({valor_a})({valor_c}))

  √{discriminante} = {math.sqrt(discriminante)}
  """)
  print(f"Las soluciones son: {numerador_solucion_1}/{denominador_solucion_1} = {solucion_1} y {numerador_solucion_2}/{denominador_solucion_2} = {solucion_2}")
  lcd.clear()
  lcd.putstr(f"Sol1={solucion_1}")
  lcd.move_to(0,1)
  lcd.putstr(f"Sol2={solucion_2}")
  ledverde.value(1)
  utime.sleep(2)
  ledverde.value(0)

