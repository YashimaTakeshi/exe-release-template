# exe-release-template

`main`にpushすると、GitHub ActionsのWindowsランナーがWindows用の`.exe`をビルドし、
Releasesに添付するところまで自動で行う最小構成のテンプレートです。

**手元にWindows環境が無くてもexeが作れます**（ランナーが本物のWindowsのため）。
スマホからコードの修正を指示してpushするだけで、配布物が出来上がります。

## 実測（tkinterのhello-world相当・2事例）

| 項目 | 実測値 |
|---|---|
| ビルド〜Release公開まで | 43〜55秒 |
| 生成されたexeのサイズ | 11.1MB |

依存ライブラリが増えればこれより伸びます。上の値は下限とみなしてください。

## 使い方

1. このリポジトリをテンプレートとしてコピーする
2. `app.py` を自分のアプリに差し替える（依存ライブラリがあれば `requirements.txt` を置く）
3. `main` にpushする
4. Actionsタブでビルドを確認し、Releasesページからexeをダウンロードする

## 仕組み

`.github/workflows/build-exe.yml` が以下を行います。

1. Windowsランナーを起動し、Python 3.12をセットアップ
2. PyInstallerと`requirements.txt`の依存関係をインストール
3. 版番号とビルド日を `build_info.py` として生成（アプリ内に表示される）
4. `pyinstaller --onefile --windowed` でexeを生成
5. サイズを検査（1MB未満ならビルド失敗とみなして停止）
6. Releasesに `v0.1.<実行番号>` として公開

アプリ側は生成された版情報を読むだけです。ローカル実行時は`build_info.py`が無いので
自動的に「dev」表示になります。

```python
try:
    from build_info import VERSION, BUILT_AT
except ImportError:
    VERSION, BUILT_AT = "dev", "ローカル実行"
```

## 注意点

- **CIが保証するのは「exeが生成された」ことまで。** Windowsで実際に起動するかは、
  ダウンロードして一度試すまで分かりません。配布前に必ず実機で起動確認してください
- `permissions: contents: write` が無いとRelease作成が403で失敗します
- `--prerelease` を付けると `releases/latest` に出なくなります（APIのlatestはprereleaseを除外するため）
- pushのたびにReleaseが作られます。タグを打ったときだけにしたい場合は、
  workflowのトリガーを `on: push: tags: ['v*']` に変更してください
- exeはウイルス対策ソフトに誤検知されることがあります。開発中の反復は
  Pythonのまま実行し、配布段階でexe化するのが定石です
