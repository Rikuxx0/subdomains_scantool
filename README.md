# SubDomains ScanTool

このツールは、偵察フェーズ（Reconnaissance）からアクティブスキャン（Active Scanning）を一気通貫で自動化するパイプラインです。サブドメインの収集、死活確認、URL探索、そして既知の脆弱性（CVE）や不適切な設定、リンク切れの診断を効率的に実行します。

また、このツールはAntigravityを使用して作成されました。

## 構成
- **偵察フェーズ**: `subfinder`, `github-subdomains`, `subBrute`, `httpx`, `waybackurls`, `katana`
- **解析・スキャンフェーズ**: `wafw00f`, `subzy`, `nuclei`, `NucleiFuzzer`

## セットアップ

### 1. 依存ツールのインストール
`go` と `python3` が必要です。以下のスクリプトは Python 仮想環境と、基本実行に必要な Go ツールをインストールします。途中で必須ツールのインストールに失敗した場合は、その場で停止します。

```bash
./install_tools.sh
source .venv/bin/activate
export PATH="$(go env GOPATH)/bin:$PATH"
```

`github-subdomains`、`subzy`、`nuclei` のインストールに失敗した場合は警告を表示します。GitHub トークン使用時は `github-subdomains`、`--active` 使用時は `nuclei` が必要です。SubBrute と NucleiFuzzer はこのスクリプトではインストールしません。

実行前に不足している必須ツールがあれば、ツール名を表示して終了します。外部コマンドが途中で失敗した場合も終了コード 1 で停止します。

## 使い方

### 基本実行（このモードではパッシブスキャンを使用しています。）
ターゲットドメインを指定して実行します。結果はデフォルトで `outputs/` ディレクトリに保存されます。

```bash
python3 recon_to_scan.py -d example.com
```

### アクティブスキャンを含む実行 
#### 注意: このモードはアクティブスキャンのため、環境に対して影響を及ぼす可能性があります。
`--active` フラグを付与すると、Nuclei等による脆弱性スキャンも実行されます。

```bash
python3 recon_to_scan.py -d example.com --active
```

### GitHubトークンの使用
GitHubからサブドメインを収集したい場合は、GitHubトークンを指定します。

```bash
python3 recon_to_scan.py -d example.com -t YOUR_GITHUB_TOKEN
```

## 出力ファイル
- `outputs/domain.txt`: 重複排除されたサブドメインリスト
- `outputs/alive.txt`: 死活確認済みのホスト（ステータスコード付き）
- `outputs/all_urls.txt`: 収集された全URLリスト
- `outputs/nuclei_results.txt`: Nucleiのスキャン結果
- `outputs/broken_links.txt`: リンク切れ診断結果（Broken Link Hijacking）

## 免責事項
本ツールは教育およびセキュリティ診断の目的で作成されています。許可を得ていない対象に対して実行することは法律で禁じられている場合があります。自己責任で使用してください。
