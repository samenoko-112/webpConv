import os
from PIL import Image
import flet as ft

# PNG -> WebP 変換関数
def convert_all_png_to_webp(input_dir, update_status, update_progress, total_files):
    processed_files = 0
    for filename in os.listdir(input_dir):
        if filename.endswith('.png'):
            input_image_path = os.path.join(input_dir, filename)
            output_image_path = os.path.join(input_dir, filename.replace('.png', '.webp'))
            with Image.open(input_image_path) as img:
                img.save(output_image_path, 'webp')

            # 進捗状況を更新
            processed_files += 1
            progress = processed_files / total_files  # 0.0 ~ 1.0 の範囲で進捗を計算
            update_status(f'{filename} を {output_image_path} に変換しました。')
            update_progress(progress)

def main(page: ft.Page):
    page.title = "PNG -> WebP Converter"

    # ディレクトリ選択結果を表示するテキスト
    selected_dir = ft.Text(value="選択されたディレクトリ: なし", size=18)

    # ステータス更新用のフィールド
    status_output = ft.Text(value="待機中", size=16)

    # プログレスバー
    progress_bar = ft.ProgressBar(value=0.0)

    # ディレクトリ選択ボタン
    def pick_directory(e):
        dir_picker.get_directory_path()

    # ディレクトリが選択されたときに実行される関数
    def select_directory(e: ft.FilePickerResultEvent):
        if e.path:
            selected_dir.value = f"選択されたディレクトリ: {e.path}"
            page.update()

    # 変換ボタンを押したときの処理
    def start_conversion(e):
        if "なし" not in selected_dir.value:
            dir_path = selected_dir.value.split(": ")[1]

            # ディレクトリ内のPNGファイルをカウント
            png_files = [f for f in os.listdir(dir_path) if f.endswith('.png')]
            total_files = len(png_files)
            if total_files == 0:
                status_output.value = "変換するPNGファイルが見つかりません。"
                page.update()
                return

            # 進捗を0にリセット
            update_progress(0.0)

            # PNG -> WebP 変換の実行
            convert_all_png_to_webp(dir_path, update_status, update_progress, total_files)
        else:
            status_output.value = "ディレクトリを選択してください。"
            page.update()

    # 進行状況を更新する関数
    def update_status(message):
        status_output.value = message
        page.update()

    # プログレスバーを更新する関数
    def update_progress(value):
        progress_bar.value = value
        page.update()

    # FilePickerをページに追加
    dir_picker = ft.FilePicker(on_result=select_directory)
    page.overlay.append(dir_picker)

    # GUI要素の作成
    convert_button = ft.ElevatedButton(text="PNGをWebPに変換", on_click=start_conversion)
    dir_button = ft.ElevatedButton(text="ディレクトリを選択", on_click=pick_directory)

    # ページのレイアウト（要素の順序を調整）
    page.add(
        selected_dir,
        dir_button,
        convert_button,
        status_output,  # 変換状況のメッセージ
        progress_bar    # プログレスバーは最後に表示
    )

# Fletアプリの開始
ft.app(target=main)
