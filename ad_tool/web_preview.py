import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .agents import AccountStructuringAgent, CreativeGenerationAgent, ProjectPlanningAgent
from .models import AdInput, Budget, CreativeAsset, Schedule, TargetingSegment


def _build_ad_input(payload: dict) -> AdInput:
    targeting = [
        TargetingSegment(name=item.get("name", "兴趣受众"), countries=item.get("countries", ["US"]))
        for item in payload.get("targeting", [])
    ]
    creatives = [
        CreativeAsset(
            asset_id=item.get("asset_id", "manual_001"),
            type=item.get("type", "image"),
            size=item.get("size", "1080x1080"),
            headline=item.get("headline", "默认标题"),
            text=item.get("text", "默认文案"),
            source=item.get("source", "manual"),
            url=item.get("url"),
        )
        for item in payload.get("creatives", [])
    ]
    return AdInput(
        channel=payload.get("channel", "meta"),
        ad_account_id=payload.get("ad_account_id", "act_demo_001"),
        schedule=Schedule(
            start_time=payload.get("start_time", "2026-03-01T08:00:00+08:00"),
            end_time=payload.get("end_time", "2026-03-15T23:00:00+08:00"),
        ),
        budget=Budget(currency=payload.get("currency", "USD"), total=float(payload.get("budget_total", 500))),
        targeting=targeting,
        creatives=creatives,
    )


HTML = """<!doctype html><html><head><meta charset='utf-8'/><title>AI Ad Preview</title>
<style>body{font-family:Arial;margin:20px;background:#f7f7fb}section{background:#fff;padding:16px;border-radius:8px;margin-bottom:12px}textarea,input,select{width:100%;margin:6px 0;padding:8px}button{padding:8px 12px;background:#3b82f6;color:#fff;border:0;border-radius:6px;cursor:pointer}.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}pre{background:#111;color:#ddd;padding:10px;border-radius:6px;max-height:260px;overflow:auto}</style>
</head><body>
<h1>AI 广告全流程本地预览</h1>
<section><h3>Page1: 输入链接</h3><input id='product_url' placeholder='https://shop.example.com/shoe-ultra-1'/><input id='channel' value='meta'/><input id='budget' value='600'/><button onclick='plan()'>生成推荐</button></section>
<section class='grid'><div><h3>Page2: 基础信息</h3><input id='ad_account_id' placeholder='ad account'/><input id='start_time' placeholder='start_time'/><input id='end_time' placeholder='end_time'/><textarea id='targeting' rows='4' placeholder='每行一个受众，例如：兴趣受众'></textarea><h4>素材</h4><textarea id='manual_creatives' rows='5' placeholder='手动素材文案，一行一个 headline|text'></textarea><button onclick='genCreative()'>AI 生成素材</button><div id='ai_creatives'></div><button onclick='buildStructure()'>生成页面3结构</button></div><div><h3>Page3: 结构预览</h3><pre id='output'>{}</pre><button onclick='submitCreate()'>提交创建(模拟)</button><div id='create_msg'></div></div></section>
<script>
let latestPlan=null; let latestAICreatives=[];
async function post(url,data){const r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});return await r.json();}
async function plan(){const data=await post('/api/plan',{product_url:product_url.value,channel:channel.value,budget:parseFloat(budget.value)});latestPlan=data;ad_account_id.value=data.result.page2_defaults.ad_account_id;start_time.value=data.result.page2_defaults.schedule.start_time;end_time.value=data.result.page2_defaults.schedule.end_time;targeting.value=data.result.hidden_recommendations.targeting.map(t=>t.segment).join('\n');output.textContent=JSON.stringify(data,null,2);}
async function genCreative(){const title=latestPlan?latestPlan.result.product_summary.title:'商品';const data=await post('/api/creative',{product_title:title,channel:channel.value,sizes:['1080x1080','1080x1920'],count:3});latestAICreatives=data.result;ai_creatives.innerHTML=latestAICreatives.map((c,i)=>`<label><input type='checkbox' checked id='c${i}'/>${c.headline}</label>`).join('<br/>');}
function selectedCreatives(){const out=[];for(let i=0;i<latestAICreatives.length;i++){if(document.getElementById('c'+i)?.checked)out.push(latestAICreatives[i]);}
const manual=manual_creatives.value.trim();if(manual){manual.split('\n').forEach((line,idx)=>{const [h,t]=line.split('|');out.push({asset_id:'manual_'+idx,type:'image',size:'1080x1080',headline:h||'手动标题',text:t||'手动文案',source:'manual'});});}
return out;}
async function buildStructure(){const tlist=targeting.value.split('\n').filter(Boolean).map(n=>({name:n,countries:['US']}));const data=await post('/api/structure',{channel:channel.value,ad_account_id:ad_account_id.value,start_time:start_time.value,end_time:end_time.value,budget_total:parseFloat(budget.value),targeting:tlist,creatives:selectedCreatives()});output.textContent=JSON.stringify(data,null,2);}
async function submitCreate(){const data=await post('/api/create_mock',{});create_msg.textContent=data.message;}
</script></body></html>"""


class PreviewHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        body = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            if self.path == "/api/plan":
                payload = self._read_json()
                result = ProjectPlanningAgent().run(
                    product_url=payload.get("product_url", ""),
                    channel=payload.get("channel", "meta"),
                    budget_total=float(payload.get("budget", 500)),
                )
                self._send_json(result)
                return
            if self.path == "/api/creative":
                payload = self._read_json()
                result = CreativeGenerationAgent().run(
                    product_title=payload.get("product_title", "商品"),
                    channel=payload.get("channel", "meta"),
                    sizes=payload.get("sizes", ["1080x1080"]),
                    count=int(payload.get("count", 3)),
                )
                self._send_json(result)
                return
            if self.path == "/api/structure":
                payload = self._read_json()
                ad_input = _build_ad_input(payload)
                result = AccountStructuringAgent().run(ad_input)
                self._send_json(result)
                return
            if self.path == "/api/create_mock":
                self._send_json({"message": "已交给工程媒体API创建链路（此处仅模拟）"})
                return
            self.send_error(404)
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=400)


def run_preview_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), PreviewHandler)
    print(f"Preview server running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_preview_server()
