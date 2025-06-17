from df.enhance import enhance, init_df, load_audio
import torch
import numpy as np
import soundfile as sf
import os

# Инициализация при старте
model, df_state, _ = init_df()

def denoise_audio(file_path: str) -> np.ndarray:
    audio, _ = load_audio(file_path, sr=df_state.sr())  # Загружаем с нужной частотой
    enhanced = enhance(model, df_state, audio)
    return enhanced.squeeze()  # [1, N] → [N]