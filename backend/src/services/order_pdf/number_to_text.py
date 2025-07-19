def convert_number_to_text(final_amount: float) -> str:
    unidades = ['', 'UN', 'DOS', 'TRES', 'CUATRO', 'CINCO', 'SEIS', 'SIETE', 'OCHO', 'NUEVE']
    decenas = ['', 'DIEZ', 'VEINTE', 'TREINTA', 'CUARENTA', 'CINCUENTA', 'SESENTA', 'SETENTA', 'OCHENTA', 'NOVENTA']
    especiales_diez_a_veinte = ['DIEZ', 'ONCE', 'DOCE', 'TRECE', 'CATORCE', 'QUINCE', 'DIECISÉIS', 'DIECISIETE', 'DIECIOCHO', 'DIECINUEVE']
    centenas = ['', 'CIENTO', 'DOSCIENTOS', 'TRESCIENTOS', 'CUATROCIENTOS', 'QUINIENTOS', 'SEISCIENTOS', 'SETECIENTOS', 'OCHOCIENTOS', 'NOVECIENTOS']

    def number_to_short_text(num: int) -> str:
        if num == 0:
            return ''
        if num < 10:
            return unidades[num]
        if 10 <= num < 20:
            return especiales_diez_a_veinte[num - 10]
        if 20 <= num < 100:
            texto = decenas[num // 10]
            if num % 10 != 0:
                texto += ' Y ' + unidades[num % 10]
            return texto
        if 100 <= num < 1000:
            centena = num // 100
            resto = num % 100
            if centena == 1 and resto == 0:
                return 'CIEN'
            texto = centenas[centena]
            if resto > 0:
                texto += ' ' + number_to_short_text(resto)
            return texto
        return ''

    def number_to_text_miles(num: int) -> str:
        if num < 1000:
            return number_to_short_text(num)
        if num < 10000:
            miles = num // 1000
            resto = num % 1000
            texto = 'MIL' if miles == 1 else unidades[miles] + ' MIL'
            if resto > 0:
                texto += ' ' + number_to_short_text(resto)
            return texto
        if num < 100000:
            decenas_mil = num // 1000
            resto = num % 1000
            texto = ''
            if decenas_mil < 20:
                texto = number_to_short_text(decenas_mil) + ' MIL'
            else:
                decenas_valor = (decenas_mil // 10) * 10
                unidades_mil = decenas_mil % 10
                if decenas_valor == 10:
                    texto = especiales_diez_a_veinte[unidades_mil] + ' MIL'
                elif decenas_valor == 20:
                    texto = 'VEINTE' + (' Y ' + unidades[unidades_mil] if unidades_mil > 0 else '') + ' MIL'
                else:
                    texto = decenas[decenas_mil // 10] + (' Y ' + unidades[unidades_mil] if unidades_mil > 0 else '') + ' MIL'
            if resto > 0:
                texto += ' ' + number_to_short_text(resto)
            return texto
        return ''

    if final_amount < 0:
        return 'El monto debe ser un número positivo.'

    final_amount = round(final_amount * 100) / 100
    parte_entera = int(final_amount)
    parte_decimal = int(round((final_amount - parte_entera) * 100))

    if parte_entera == 0:
        texto_entero = 'CERO'
    elif parte_entera < 100000:
        texto_entero = number_to_text_miles(parte_entera)
    else:
        texto_entero = 'CANTIDAD FUERA DE RANGO'

    texto_entero = texto_entero.upper()

    return f"SON: {texto_entero} CON {parte_decimal:02d}/100 SOLES"