from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import *
from django.template.context import RequestContext
import settings
from django.shortcuts import get_object_or_404
import requests
from settings import *

ERR_QUERY_NOT_FOUND='<h1>Query not found</h1>'
ERR_IMG_NOT_AVAILABLE='The requested result can not be shown now'

def home(request):
    if request.method == 'POST':
        q = request.POST.get('q',None)
        start=request.POST.get('start',0)
        if q != None and len(q) > 2:
            return search(request,q,start)
        else:
            if q==None:
                return render_to_response('rsc/index.html',{'errormessage':None},context_instance=RequestContext(request))
            else:
                errormessage='Please use larger queries'
                return render_to_response('rsc/index.html',{'errormessage':errormessage},context_instance=RequestContext(request))
    else: # it's a get request, can come from two sources. if start=0, or start not in GET dictionary, someone is requesting the page 
          #for the first time, else  something like "show more" 
       start=int(request.GET.get('start',0))
       query=request.GET.get('q',None)
       if start==0 or query==None:
           return render_to_response('rsc/index.html',context_instance=RequestContext(request))
       else:
           return search(request,query,start)
                

def search(request,query,start):
        apibaseurl=BASEURL+"/api/apollo/solr/"+COLLECTION+'/select?q='+query+"&fl=title,content,id,url,keywords&wt=json&"
        cred=(USERNAME,PASSWORD)
        hlstr='hl=true&hl.fl=keywords,content&hl.simple.pre=<span style="color:blue">&hl.simple.post=</span>&hl.usePhraseHighlighter=true&hl.highlightMultiTerm=true'
        apiurl=apibaseurl+hlstr+"&start="+str(start)
        try:
            r = requests.get(apiurl,auth=cred)
        except requests.ConnectionError:
            return render_to_response('rsc/error.html',{'errormessage':'We are having connection problems, please try later.'}\
            ,context_instance=RequestContext(request))
        if r.status_code!=200:
            return render_to_response('rsc/error.html',{'errormessage':'Your query returned zero results, please try another query'}\
            ,context_instance=RequestContext(request))
        else:
            print "search done"
            totalresultsNumFound= r.json()['response']['numFound']
            hlresults=r.json()['highlighting']
            results=r.json()['response']['docs']
            HTMLResults=[]
            if len(results) > 0:
                for result in results:
                    htmlid=result['id'].encode('utf8')                     
                    f = HTMLResult(htmlid)
                    if len(result.get('title',[])) > 0:
                        f.title=result['title'][0].encode("utf-8")
                    if len(result.get('content',[])) > 0:
                        content=result['content'][0].encode("utf-8")
                        if len(content.split(" "))>50:
                            f.lesscontent=' '.join(content.split(" ")[:50])
                        else:
                            f.lesscontent=None     
                        f.content=content
                    if len(result.get('url',""))>0:
                        f.url='"'+result['url'].encode("utf-8")+'"'
                    if len(result.get('keywords',""))>0:
                        f.keywords=result['keywords'].encode('utf-8')
                    if "keywords" in hlresults[result['id']]:
                        f.keywords=hlresults[result['id']]['keywords'][0].encode("utf-8")
                    if "content" in hlresults[result['id']]:
                        f.lesscontent=hlresults[result['id']]['content'][0].encode("utf-8")
                    HTMLResults.append(f)
                return render_to_response('rsc/htmlresult.html', {'results':HTMLResults ,'q': query,\
							  'total':totalresultsNumFound, 'i':str(start+1)\
							  , 'j':str(len(results)+start) },context_instance=RequestContext(request))
            else:
               return render_to_response('rsc/error.html',{'errormessage':'Your search returned zero results, please try another query'}\
            ,context_instance=RequestContext(request))
				
	


