# ESP32 RSS Display

ESP32-WROVER-EでRSSサイトにアクセスし、記事のタイトルと概要をディスプレイに表示するプログラムです。

## 開発の動機

[ラズパイPico版](https://github.com/led-mirage/RaspiPicoW-RSSDisplay)では大きなRSSデータを読み込むとメモリ不足でエラーになる場合がありました（Picoのメインメモリは264KB）。ESP32-WROVER-Eは疑似SRAM（PSRAM）が搭載されており、それを使うことでこの問題が解決できるのかどうかを確かめました（ESP32-WROVER-Eのメインメモリは520KB、PSRAMは8MB）。

## 機能概要

- プログラム内で指定したRSSサイトにアクセスし、タイトルと記事の概要を順次表示します（過去2日分に限定）
- タクトスイッチを押すとフォントサイズが切り替わります(3段階)

※ラズパイPico版と比べると、表示する記事を過去２日分に限定する機能が追加されています。

## 使用パーツ

- ESP32-DevKitC-VE ESP32-WROVER-E開発ボード … 1,750円（税込）
- 有機ELディスプレイ SSD1306 … 580円（税込）
- タクトスイッチ … 30円（税込）
- ブレッドボード（6穴版） … 460円（税込）
- 配線用のワイヤー

合計：2,820円（税込）

## 配線図

![wire](https://github.com/led-mirage/ESP32-RSSDisplay/assets/139528700/c3663804-314a-40d8-8c31-e616bfc7ad4b)

## 実行画面

https://github.com/led-mirage/ESP32-RSSDisplay/assets/139528700/315f5483-b38b-4961-a40e-3d4392e313b2

## 開発環境

- Thonny 4.0.2
- Windows 10 / 11

## 実行環境

- ESP32-DevKitC-VE ESP32-WROVER-E開発ボード
- MicroPython v1.20.0 (ESP32 with SPIRAM)

## インストール

PCとESP32-WROVER-Eを接続して、以下のファイルをPicoにコピーしてください。Thonnyを使うと簡単です。

```
  main.py [メインプログラム]
  date.py [日付処理用モジュール]
  ntp.py [NTPモジュール]
  ssd1306.py [ssd1306用ドライバ]
  ssd1306_mfont.py [ssd1306用ドライバ拡張]
  mfont [フォントライブラリ（外部ライブラリ）]
    │  mfont.py [フォントドライバモジュール]
    │  tma_jp_utl.py [フォントモジュール用サブルーチン]
    │  __init__.py [フォントドライバモジュール用]
    └─ fonts [フォントファイル]
            u_12x12.fnt [東雲フォント(12ドット)]
            u_14x14.fnt [東雲フォント(14ドット)]
            u_16x16.fnt [東雲フォント(16ドット)]
```

※mfontフォルダ以下はTamakichiさん作成のライブラリです。  
以下のリンクから別途ダウンロードしてください。  
https://github.com/Tamakichi/pico_MicroPython_Multiifont  
fontsフォルダのフォントは、オリジナルのフォルダの中から12、14、16ドットフォントを抜粋してインストールします。

## WiFiアクセスポイントの設定

main.pyの先頭部分にある以下の設定をお使いの環境に合わせて書き換えてください。アクセスポイントを複数記載してある場合は、上から順次接続を試みます。

```py
# WiFiアクセスポイント
WIFI_ACCESS_POINTS = [
    {"ssid": "ssid_A", "password": "pass_A"},
    {"ssid": "ssid_B", "password": "pass_B"},
    ]
```

## RSSサイトの設定

main.pyの先頭部分にある以下の設定を、閲覧したいRSSサイトに合わせて編集してください。

```py
# RSSサイト
RSS_SITES = [
    {"name": "NHK主要ニュース", "url": "https://www.nhk.or.jp/rss/news/cat0.xml"},
    {"name": "CNET Japan", "url": "http://feeds.japan.cnet.com/rss/cnet/all.rdf"},
    {"name": "GIGAZINE", "url": "https://gigazine.net/news/rss_2.0/"},
    {"name": "ITMedia 科学", "url": "https://rss.itmedia.co.jp/rss/2.0/news_technology.xml"},
    {"name": "ITMedia セキュリティ", "url": "https://rss.itmedia.co.jp/rss/2.0/news_security.xml"},
    {"name": "ITMedia 国内", "url": "https://rss.itmedia.co.jp/rss/2.0/news_domestic.xml"},
    ]
```

## 実行

電源を入れると自動的に実行されます。

## 外部ライブラリ

このプログラムは以下の外部ライブラリを使用しています。これらの外部ライブラリのライセンスに関してはそれぞれのプロジェクトをご参照ください。

- ssd1306.py  
  [micropython-ssd1306](https://github.com/stlehmann/micropython-ssd1306)
- mfontフォルダ  
  [pico_MicroPython_Multiifont](https://github.com/Tamakichi/pico_MicroPython_Multiifont)

## 制限

RSSサイトから配信されるXMLが適度に改行されていないと、正常に動作しません。この制限はこの独自のパースロジックに由来するものです。例えばCNNが配信しているRSSデータは、このプログラムでは正常にパース出来ません。これはCNNのデータに問題があるわけではなく、単にこのプログラムの制限事項です。

## 附録．開発の準備

ラズパイPicoと比べるとESP32-WROVER-Eは開発を始めるのが面倒だったので、備忘録代わりに留意点を記載しておきます。

### ESP32-WROVER-Eを使うためのPC側の準備

#### Pythonのインストール

次に述べるesptoolをインストールするために、まずはPythonをインストールする必要があります。ここではPythonの[公式サイト](https://www.python.org/)からダウンロードしたバージョン3.11.4を使用しました。

#### esptoolのインストール

PCとESP32をUSBケーブルで接続した後、Windowsのコマンドプロンプトを起動し、次のように入力し、esptoolをインストールします。

```
> pip install esptool
```

インストール後、次のコマンドを実行するとESP32のチップの情報が表示されます。

```
> esptool flash_id
```

もしESP32とうまく通信できない場合は、PCに適切なUSBドライバがインストールされていない可能性があります。その場合は、次の項目を参照しUSBドライバをインストールしてください。

#### USBドライバのインストール

デバイスマネージャーで確認すると以下のようなデバイスが見つかると思います。

Silicon Labs CP210x USB to UART Bridge

Silicon Labsの[公式ページ](https://jp.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads)から、利用している環境のドライバをダウンロードし（ここではWindows用のCP210x Universal Windows Driverをダウンロードしました）、解凍してできた
silabser.infファイルを右クリックして「インストール」すれば完了です。

インストール後、再度下記コマンドを実行すればチップの情報が表示されるはずです。

```
> esptool flash_id
```

### ESP32へのMicroPythonファームウェアの書き込み

#### ファームウェアのダウンロード

MicroPythonの[公式ページ](https://micropython.org/download/esp32spiram/)から使用するファームウェアをダウンロードします。ここでは疑似SRAMを使いたいので、「ESP32 with SPIRAM」というファームウェアをダウンロードします。

#### フラッシュメモリのクリア

まず、フラッシュメモリをクリアするために以下のコマンドを実行します。--portの後のCOMポートはPCとESP32を接続しているCOMポートを記載してください。接続しているCOMポートは上記「esptool flash_id」コマンドで確認できます。

```
> esptool --chip esp32 --port COM7 erase_flash
```

#### ファームウェアの書き込み

以下のコマンドでファームウェアをESP32に書き込みます。先ほどと同様に--portオプションには使用しているCOMポートを、一番最後のファイル名にはダウンロードしたMicroPythonのファームウェアファイル名を指定してください。

```
> esptool --chip esp32 --port COM7 --baud 460800 write_flash -z 0x1000 esp32spiram-20230426-v1.20.0.bin
```

#### メモリ量の確認

ファームウェアの書き込みが終わったら、Thonnyなどの開発環境を起動してESP32と接続し、REPLで以下のコマンドを実行してメモリ量を確認します。正常に疑似SRAMを認識できていれば、4MB程度の空き容量が表示されるはずです。

```py
>>> import gc
>>> gc.mem_free()
4088800
```

ESP32-WROVER-Eの[データシート](https://akizukidenshi.com/download/ds/espressifsystems/esp32-wrover-e_esp32-wrover-ie_datasheet_en.pdf)にはPSRAMは8MBと記載されていますが、上記の通りここで利用できるのは4MB程度となっています。この差がどこから生まれるのかは不思議ですが、4MBもあればRSSを解析する分には問題ないです。

## バージョン履歴

### 1.2 (2023/07/30)
- ファーストリリース
- ラズパイPico版からの分岐
