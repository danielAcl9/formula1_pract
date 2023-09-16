def maximizar_valor_mochila(capacidad_maxima, valores, pesos):
    n = len(valores)
    dp = [[0 for _ in range(capacidad_maxima + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacidad_maxima + 1):
            if pesos[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - pesos[i - 1]] + valores[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    # Recuperar la solución óptima (elementos seleccionados)
    seleccionados = []
    i, j = n, capacidad_maxima
    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            seleccionados.append(i - 1)
            j -= pesos[i - 1]
        i -= 1

    seleccionados.reverse()
    return dp[n][capacidad_maxima], seleccionados

# Ejemplo de uso:
capacidad_maxima = 100
# puntos = [649, 453, 351, 321, 245, 235, 188, 177, 132, 130, 109, 84, 82, 74, 71, 62, 57, 44, 24, -4]
puntos_modelo = [5, 6, 3, 8, 7, 2, 1, 4, 9, 16, 17, 19, 20, 11, 12, 10, 14, 15, 13, 18]
precios_f = [29, 21, 25, 13, 20, 19, 22, 15, 11, 10, 10, 9, 6, 8, 9, 11, 5, 5, 5, 5]
# precios = [28, 20, 25, 13, 19, 18, 22, 15, 10, 10, 10, 8, 5, 7, 8, 11, 5, 4, 5, 4]
max_valor, elementos_seleccionados = maximizar_valor_mochila(capacidad_maxima, puntos_modelo, precios_f)

print("El valor total de puntos que puedo tener es:", max_valor)
print("Conductores seleccionados (índices):", elementos_seleccionados)
