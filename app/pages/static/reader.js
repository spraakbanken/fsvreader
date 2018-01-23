function foreach(elems, f) {
  for (var i = 0; i < elems.length; i++) {
    //console.log("loop", i, elems[i])
    f(elems[i])
  }
}
function get(url, k) {
  const r = new XMLHttpRequest()
  r.onreadystatechange = function() {
    if (r.readyState == 4 && r.status == 200) {
      k(r.responseText)
    }
  }
  r.open('GET', url, true)
  r.send(null)
}
window.main = function(textframe_url, lexurl) {
  get(textframe_url, function(d) {
    var fsvtext = document.getElementById('fsvtext')
    fsvtext.innerHTML = d

    var textitems = fsvtext.getElementsByTagName('a')
    foreach(textitems, function(a) {
      a.onclick = function(e) {
        e.preventDefault() // ta bort
        console.log('click on', e.target)
        console.log('link to', a.className)
        links = a.className.replace(/(?:^|\s)underline(?:$|\s)/, ' ').trim()
        console.log('link on', links)
        links = links.replace(/(?:^|\s)hl(?:$|\s)/, ' ')
        console.log('link on', links)
        links = links.replace(/\s+/g, '--')
        console.log('link on', links)
        removeclass('underline')
        removeclass('highlight')
        e.target.className += ' underline'
        load_lex(lexurl + links)
      }
    })
    console.log('klar')
  })
}
function load_lex(url) {
  document.getElementById('lexframe').innerHTML = '<div class="sk-fading-circle"> <div class="sk-circle1 sk-circle"></div> <div class="sk-circle2 sk-circle"></div> <div class="sk-circle3 sk-circle"></div> <div class="sk-circle4 sk-circle"></div> <div class="sk-circle5 sk-circle"></div> <div class="sk-circle6 sk-circle"></div> <div class="sk-circle7 sk-circle"></div> <div class="sk-circle8 sk-circle"></div> <div class="sk-circle9 sk-circle"></div> <div class="sk-circle10 sk-circle"></div> <div class="sk-circle11 sk-circle"></div> <div class="sk-circle12 sk-circle"></div> </div>'
  get(url, function(d) {
    var lexframe = document.getElementById('lexframe')
    lexframe.innerHTML = d
    var lexitems = lexframe.getElementsByTagName('a')
    linkHighlight(lexitems)
    var ellipsHead = lexframe.getElementsByClassName('ellipsis_header')
    foreach(ellipsHead, function(a) {
      a.onclick = function(e) {
        console.log('ellipsis', e)
        console.log('parent', this.parentNode.childNodes) // .getElementsByClassName(".ellipsis_contents")
        foreach(this.parentNode.childNodes, function(e) {
          console.log('this is ', e)
          console.log('class', e.className)
          if (e.className === 'ellipsis_content') {
            console.log('toggle', e)
            toggle(e)
          }
          if (e.className === 'ellipsis_pre') {
            console.log('toggle', e)
            toggle(e)
          }
          //e.toggle()
          // e.find(".ellipsis_plus").toggle();
        })
        //.getElementsByClassName(".ellipsis_contents"), function(e) {e.toggle("slow")}
        //foreach(e.parentNode.childNodes.getElementsByClassName(".ellipsis_contents"), function(e) {e.toggle("slow")})
      }
    })
  })
}

function linkHighlight(lexitems) {
  foreach(lexitems, function(a) {
    a.onclick = function(e) {
      console.log('set', e)
      e.preventDefault() // ta bort
      console.log('classname', e.target.className)
      console.log(
        'classname 2',
        e.target.className.match(/(?!highlight)(?:^|\s)\S+/g)
      )
      foreach(e.target.className.match(/(?!highlight)(?:^|\s)\S+/g), hl)
    }
  })
}
function toggle(x) {
  console.log('toggle it', x, x.style.display)
  if (x.style.display === 'block') {
    x.style.display = 'none'
  } else {
    x.style.display = 'block'
  }
}

function hl(s) {
  console.log('hl running')
  removeclass('highlight')
  var frameDoc = document.getElementById('fsvtext')
  console.log('find by class', s)
  var as = frameDoc.getElementsByClassName(s)
  console.log('iframe', as)
  foreach(as, function(a) {
    a.className += ' highlight'
  })
}

function removeclass(s) {
  console.log('remove', s)
  var frameDoc = document.getElementById('fsvtext')
  var hls = frameDoc.getElementsByClassName(s)
  var hlscopy = []
  foreach(hls, function(h) {
    hlscopy.push(h)
  })
  foreach(hlscopy, function(a) {
    console.log('innan', a.className)
    a.className = a.className.replace(
      new RegExp('(?:^|\\s)' + s + '(?:\\s|$)'),
      ' '
    )
    console.log('efter', a.className)
  })
}
