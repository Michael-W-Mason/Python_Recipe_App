function getRecipe(id){
    fetch('http://localhost:5000/recipes/' + id)
    .then(res => res.json())
    .then(data => {
        formatModal(data.data)
    });

}

function formatModal(data){
    let modalTitle = document.getElementById('recipeModalLabel');
    let modalDesc = document.getElementById('recipeModalDesc');
    let modalServes = document.getElementById('recipeModalServes');
    let modalTime = document.getElementById('recipeModalTime');
    let modalIngredients = document.getElementById('recipeModalIngredients');
    let modalInstructions = document.getElementById('recipeModalInstructions');
    let modalImage = document.getElementById('recipeModalImage');

    modalTitle.innerText = data["name"];
    modalDesc.innerText = data["desc"];
    modalServes.innerText = `Serves: ${data["serves"]} People`;
    modalTime.innerText = `Total Cook Time (hrs): ${data["cook_time"]}`;
    modalImage.setAttribute("src", `/cdn/${data["id"]}`)

    modalIngredients.replaceChildren();
    modalInstructions.replaceChildren();
    
    for (let i of data['ingredients']) {
        let li = document.createElement('li')
        li.innerText = i
        modalIngredients.append(li)
    }
    for (let i of data['instructions']) {
        let li = document.createElement('li')
        li.innerText = i
        modalInstructions.append(li)
    }
}