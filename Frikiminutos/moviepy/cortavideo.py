from moviepy.video.io.VideoFileClip import VideoFileClip

def cortar_video(archivo_video, segundo_inicio, segundo_final):
    # Cargar el video
    video = VideoFileClip(archivo_video)

    # Cortar el video
    video_cortado = video.subclip(segundo_inicio, segundo_final)

    # Guardar el video cortado
    nombre_salida = f"{archivo_video.split('.')[0]}_cortado.webm"
    video_cortado.write_videofile(nombre_salida)

    print(f"Video cortado guardado como: {nombre_salida}")

if __name__ == "__main__":
    archivo_video = input("Ingrese el nombre del archivo de video: ")
    segundo_inicio = int(input("Ingrese el segundo de inicio del corte: "))
    segundo_final = int(input("Ingrese el segundo final del corte: "))
    cortar_video(archivo_video, segundo_inicio, segundo_final)