var main_person="[anonymous]";
function date(x){return x.slice(0,10);}
function time(x){return x.slice(11,16);}
for(var i=data.length-1;i>=0;i--){
	if(i==0||date(data[i].time)!=date(data[i-1].time))
		data.splice(i,0,{type: "date", time: date(data[i].time)});
}
const n=data.length,MAX_MSG=200;
document.getElementById('tools-idx').max=n-1;
document.getElementById('tools-idx').placeholder=`${0} ~ ${n-1}`;
const dialog=document.getElementById('dialog');
var l,r;
var t=parseInt(window.location.hash.slice(1));
if(0<=t&&t<n) l=r=t+1;
else l=r=n;
function time_str(t){
	var ss=t%60,mm=parseInt(t/60)%60,hh=parseInt(t/3600);
	if(hh==0)
		return `${parseInt(mm/10)}${parseInt(mm%10)}:${parseInt(ss/10)}${parseInt(ss%10)}`;
	return `${hh}:${parseInt(mm/10)}${parseInt(mm%10)}:${parseInt(ss/10)}${parseInt(ss%10)}`;
}
var escmap={'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'};
const escapeHTML=text=>text.replace(/[&<>"']/g,m=>escmap[m]);
function content(x){
	switch(x.type){
	case 'text':
		return `<div class="w3-tag w3-round-xlarge msg ${x.app}">
					${escapeHTML(x.msg).replace(/\n/g,'<br>')}
				</div>`;
	case 'photo':
		return `<img src="./${x.photos[0].split('/').slice(3).join('/')}" class="photo" alt="photo">`;
	case 'video':
		return `<video controls class="video"><source src="./${x.videos[0].split('/').slice(3).join('/')}"></video>`;
	case 'gif':
		return `<img src="./${x.gifs[0].split('/').slice(3).join('/')}" class="gif" alt="gif">`;
	case 'sticker':
		return `<img src="./${x.sticker.split('/').slice(1).join('/')}" class="sticker" alt="sticker">`;
	case 'audio':
		return `<audio controls class="audio"><source src="${x.audios[0].split('/').slice(3).join('/')}"></audio>`;
	case 'file':
		return `<div class="w3-tag w3-round msg w3-padding ${x.app}">
					<a href="./${x.files[0].split('/').slice(3).join('/')}" target="_blank">${x.files[0].split('/').slice(4).join('/')}</a>
				</div>`;
	case 'call':
		if(x.duration==-1){
			return `<div class="w3-tag w3-round msg w3-padding ${x.app}">
						<i class="fa fa-phone"></i>&nbsp;&nbsp;Missed Call.
					</div>`;
		}else{
			return `<div class="w3-tag w3-round msg w3-padding ${x.app}">
						<i class="fa fa-phone loc"></i>&nbsp;&nbsp;${time_str(x.duration)}
					</div>`;
		}
		// if(x.duration==)
	default:
		return `<div class="w3-tag w3-round msg w3-padding ${x.app}">
					${JSON.stringify(x)}
				</div>`;
	}	
}
function node(id){
	var res=document.createElement('div'),x=data[id];
	if(x.type=='date'){
		res.innerHTML=x.time;
		res.classList.add('date');
		return res;
	}
	res.classList.add('line','w3-row');
	if(x.user==main_person){
		res.innerHTML=`
			<div class="w3-col l3 m3 s2 w3-padding user-left"></div>
			<div class="w3-col l6 m6 s8 w3-padding msg-right w3-border-left w3-border-right w3-border-green self">
				${content(x)}
			</div>
			<div onclick="copy_link(${id});" class="w3-col l3 m3 s2 w3-padding user-right click">${x.user}<br><sub>${time(x.time)}</sub></div>
		`;
	}else{
		res.innerHTML=`
			<div onclick="copy_link(${id});" class="w3-col l3 m3 s2 w3-padding user-left click">${x.user}<br><sub>${time(x.time)}</sub></div>
			<div class="w3-col l6 m6 s8 w3-padding msg-left w3-border-left w3-border-right w3-border-green">
				${content(x)}
			</div>
			<div class="w3-col l3 m3 s2 w3-padding user-right"></div>
		`;
	}
	return res;
}
function copy_link(i){
	window.location.hash=i;
	var input=document.createElement('textarea');
	input.innerHTML=window.location.href;
	document.body.appendChild(input);
	input.select();
	var result=document.execCommand('copy');
	document.body.removeChild(input);
	return result;
}
// [l,r)
const date_top=document.getElementById('date-top');
function update_top(){if(dialog.children.length!=0) date_top.innerHTML=date(data[l].time);}
function push_l(){
	if(l==0) return false;
	dialog.insertBefore(node(--l),dialog.firstChild);
	update_top();
	return true;
}
function pop_l(){
	if(l==r) return false;
	dialog.firstChild.remove(); l++;
	update_top();
	return true;
}
function push_r(){
	if(r==n) return false;
	dialog.appendChild(node(r++));
	return true;
}
function pop_r(){
	if(l==r) return false;
	dialog.lastChild.remove(); r--;
	return true;
}
function collapse(){
	scroll_pause=true;
	while(l<r) pop_l();
	setTimeout(()=>{scroll_pause=false},50);
}
function expand(){
	scroll_pause=true;
	while(r-l>MAX_MSG) pop_l();
	while(r-l<MAX_MSG) if(!push_l()) break;
	while(r-l<MAX_MSG) if(!push_r()) break;
	setTimeout(()=>{scroll_pause=false},50);
}
expand();
function abs(x){return x>0?x:-x;}
const scroll=document.scrollingElement;
var scroll_pause=false;
window.onscroll=function(){
	if(scroll_pause) return;
	if(scroll.scrollTop<2*MAX_MSG){
		if(l==0) return;
		for(var i=0;i<MAX_MSG/10;i++) if(!push_l()) return;
		while(r-l>MAX_MSG) if(!pop_r()) return;
	}else if(abs(scroll.scrollTop-scroll.scrollHeight+window.innerHeight)<2*MAX_MSG){
		for(var i=0;i<MAX_MSG/10;i++) if(!push_r()) return;
		while(r-l>MAX_MSG) if(!pop_l()) return;
	}
}
const set={},users=[],view_as_form=document.getElementById('view-as');
data.forEach(e=>{
	if(e.user===undefined||set[e.user]=='jizz') return;
	set[e.user]='jizz'; users.push(e.user);
});
view_as_form.innerHTML+=users.map(e=>`<option value="${e}">${e}</option>`).join('\n');
const modal=document.getElementById('tools-modal');
function toggleModal(){
	if(modal.style.display=='block')
		modal.style.display='none';
	else
		modal.style.display='block';
}
toggleModal();
window.onclick=event=>{if(event.target==modal) modal.style.display='none';};
function jumptodate(){
	collapse();
	// time search
	var date=document.getElementById('tools-date').value;
	if(date!==""){
		date=new Date(date+"T00:00:00");
		date.setDate(date.getDate()+1);
		const ok=i=>i>=0&&i<n&&(new Date(data[i].time))<date;
		var ll=0,rr=n;
		while(ll+1!=rr){
			var m=parseInt((ll+rr)/2);
			if(ok(m)) ll=m;
			else rr=m;
		}
		l=r=ll+1;
	}
	expand();
}
function jumptoidx(){
	var idx=document.getElementById('tools-idx').value;
	if(idx!==""){
		idx=parseInt(idx);
		if(0<=idx&&idx<n) goto(idx);
	};
}
function switchview(){
	main_person=view_as_form.value;
	collapse(); expand();
}
const reslist=document.getElementById('tools-search-result');
function goto(i){collapse(); l=r=i+1; expand(); setTimeout(()=>{dialog.lastChild.scrollIntoView();},50);}
function search(regex){
	var key=document.getElementById('tools-search-text').value;
	var res=[];
	if(key!=''){
		var msg,t;
		for(var i=0;i<n;i++){
			msg=data[i];
			if(msg.type!='text') continue;
			if(regex){
				t=msg.msg.match(key);
				if(t===null) continue;
				res.push([i,t.index,t.index+t[0].length]);
			}else{
				t=msg.msg.indexOf(key);
				if(t==-1) continue;
				res.push([i,t,t+key.length]);
			}
		}
	}
	// console.log(res.map(i=>data[i[0]].msg));
	if(res.length==0) reslist.innerHTML=`<li>not found</li>`;
	else reslist.innerHTML=`<li>found ${res.length} results</li>`;
	reslist.innerHTML+=res.map(([i,l,r])=>{
		var t=data[i].msg;
		l=Math.min(l,40); r=Math.min(r,40);
		t=escapeHTML(t.slice(0,l))+'<span style="color: red!important;">'+escapeHTML(t.slice(l,r))+'</span>'+escapeHTML(t.slice(r,40));
		if(data[i].msg.length>40) t=t+'<span style="color: blue!important;">...more</span>';
		return `<li onclick="goto(${i}),copy_link(${i});" class="click search-li${data[i].user==main_person?' self':''}">
							<div class="search-user">${data[i].time.toString().slice(0,10)}<br>${data[i].user}</div>
							<div class="search-msg">${t.replace(/\n/g,'<br>')}</div>
						</li>`;
	}).join('');
	document.getElementById('tools-search-result').parentElement.style.display='block';
}
// document.getElementById('tools-search-button').addEventListener("click",search);
setTimeout(()=>{dialog.lastChild.scrollIntoView();},50);