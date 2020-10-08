let sort_title = document.querySelector('#sort-title')
let sort_block = document.querySelector('.sort-block')
let drop = document.querySelector('#navbarDropdownMenuLink')

async function get_data(param, order) {
  let req = await fetch(`/photos/sort?sort=${param}&order=${order}`)
  let res = await req.text()

  if (req.ok) {
    photos = document.querySelector(".card-deck")
    photos.innerHTML = res
  }
}

if (sort_block) {
  sort_block.addEventListener('click', (e) => {
    el = document.getElementById(e.target.id)
    switch (e.target.id) {
      case 'sort-title': {
        get_data('title', 'asc')
        break
      }
      case 'sort-rating': {
        get_data('count_likes', 'asc')
        break
      }
      case 'sort-date': {
        get_data('created_date', 'desc')
        break
      }
    }

    let actives = document.getElementsByClassName('active');

    for (i = 0; i < 3; i++) {
      var currentActive = actives[0];
      if (currentActive)
        currentActive.classList.remove("active");

      if (currentActive !== el)
        el.classList.add("active");
    };
  })
}

if (drop) {
  drop.addEventListener('click', () => {
    let menu = document.querySelector('.dropdown-menu')
    menu.classList.toggle('show')
  })
}