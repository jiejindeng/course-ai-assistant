const base = '/api'
async function request(path, options={}) {
  const res = await fetch(base + path, options)
  const data = await res.json().catch(()=>({detail:'服务器返回了非 JSON 内容'}))
  if (!res.ok) throw new Error(data.detail || `请求失败：${res.status}`)
  return data
}
export const api = {
  health:()=>request('/health'), papers:()=>request('/papers'), datasets:()=>request('/datasets'), reports:()=>request('/reports'),
  chat:(message,course)=>request('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message,course})}),
  material:(kind,topic,level)=>request('/study-material',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({kind,topic,level})}),
  uploadPaper:(file)=>{const f=new FormData();f.append('file',file);return request('/papers/upload',{method:'POST',body:f})},
  uploadDataset:(file)=>{const f=new FormData();f.append('file',file);return request('/datasets/upload',{method:'POST',body:f})},
  analyze:(name)=>request(`/datasets/${encodeURIComponent(name)}/analyze`),
  saveReport:(title,content)=>request('/reports',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title,content})})
}
