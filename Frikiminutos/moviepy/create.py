from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

def crear_video(imagen1, imagen2, audio):
    # Cargar las imágenes
    clip1 = ImageClip(imagen1, duration=5)  # Duración de 5 segundos para la imagen 1
    clip2 = ImageClip(imagen2, duration=5)  # Duración de 5 segundos para la imagen 2

    # Cargar el audio
    audio_clip = AudioFileClip(audio)

    # Crear el video combinando las imágenes y el audio
    video = concatenate_videoclips([clip1.set_audio(audio_clip), clip2.set_audio(audio_clip)], method="compose")

    # Guardar el video
    nombre_salida = "video_salida.mp4"
    video.write_videofile(nombre_salida, codec='libx264', audio_codec='aac', fps=24)

    print(f"Video generado y guardado como: {nombre_salida}")

if __name__ == "__main__":
    imagen1 = input("Ingrese el nombre del archivo de la primera imagen: ")
    imagen2 = input("Ingrese el nombre del archivo de la segunda imagen: ")
    audio = input("Ingrese el nombre del archivo de audio: ")
    crear_video(imagen1, imagen2, audio)
