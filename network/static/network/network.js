//create function that picks out the edit button

function edit(postid, content) {
	//SEND INFO TO SERVER TO UPDATE POST CONTENT
	fetch(`/edit/${postid}/${content}`)
	.then(response => response.json())
	.then(data => console.log(data));

}

function like(postid) {
	//SEND INFO TO SERVER TO UPDATE LIKECOUNT
	fetch(`/like/${postid}`)
	.then(response => response.json())
	.then(data => console.log(data));

}

function follow(user) {
	//SEND INFO TO SERVER TO UPDATE FOLLOW COUNT
	fetch(`/follow/${user}`)
	.then(response => response.json())
	.then(data => console.log(data));
}

function deletePost(postid) {
	//SEND INFO TO SERVER TO UPDATE FOLLOW COUNT
	fetch(`/delete/${postid}`)
	.then(response => response.json())
	.then(data => console.log(data));
}


document.addEventListener('DOMContentLoaded', () => {

	//select all Edit buttons
 	document.querySelectorAll('.editlink').forEach(button => {
 		button.onclick = () => {
 			//hide the edit button that was clicked
 			button.style.display = "none";

 			//find the parent and child elements to access needed element
 			editform = button.parentElement.parentElement.parentElement;
 			console.log(editform);
 			postcontent = editform.parentElement.childNodes[2];
 			postid = postcontent.dataset.postid;
 			child = postcontent.childNodes[1];
 			text = child.innerHTML;

 			//create new text-area element to replace innerHTML of div
 			textarea = document.createElement("TEXTAREA");
 			textarea.setAttribute("wrap", "soft");
  			textarea.setAttribute("rows", "3");
  			textarea.setAttribute("cols", "60");
  			textarea.setAttribute("autofocus", "autofocus");

  			//create a text node to populate the text area with
  			edittext = document.createTextNode(text);
  			textarea.appendChild(edittext);

  			//create submit button for text area and assign an onclick
  			changebutton = document.createElement("INPUT");
  			changebutton.setAttribute("type", "submit");
  			changebutton.setAttribute("value", "Change");
  			changebutton.setAttribute("class", "btn btn-light btn-sm");
  			changebutton.setAttribute("style", "font-size: 12px; padding: 5px;");
  			changebutton.setAttribute("value", "Change");
  			changebutton.onclick = function(){
  				//get text
  				text = textarea.value;
  				newtext = document.createElement('a');
  				newtext.text = text;

  				//make edit button visible again after edit submitted
  				button.style.display = "block";
  				//replace the textarea with just text
  				postcontent.replaceChild(newtext, textarea);
  				postcontent.removeChild(changebutton);

  				//send this info to server
				edit(postid, text);
  			};
 			postcontent.replaceChild(textarea,child);
 			postcontent.appendChild(changebutton)
 			
 		 }

 	});

 	//select all like buttons
 	likebutton = document.querySelectorAll('.likebutton');
 	if (likebutton) {
 		likebutton.forEach(button => {
 		button.onclick = () => {

 			//get info from data-set property of button	
 			userid = button.dataset.userid;
 			postid = button.dataset.postid;

 			//locate likecounter element as child
 			parent = button.parentElement;
 			child = parent.childNodes[2];
 			likecount = child.innerHTML;
 			icon = button.childNodes[1]; 			

 			//toggle btw like icon and Unlike icon
 			if (icon.className == "far fa-heart") {
 				icon.className = "fa-solid fa-heart" ;
 				likecount = parseInt(likecount) + 1;
 			}
 			else {
 				icon.className = "far fa-heart";
 				likecount = parseInt(likecount) - 1;
 			}
 			//update like counter
 			child.innerHTML = likecount;

 			//send to server
 			like(postid);
 			
 		}
 		
 	});
 	} 


 	//select the follow button
 	followbutton = document.querySelector('#follow');
 	if (followbutton) {
 		followbutton.onclick = function () {
 		//know the user who wants to follow
 		const user2 = this.dataset.userid;
 		numFollowers = document.querySelector('#num_followers');
 		numFollow = parseInt(numFollowers.innerHTML);

 		//toggle the follow button
 		if (this.dataset.following === 'True') {
 			numFollow -= 1;
 			this.dataset.following = 'False';
 			//change content of button
 			this.innerHTML = '<i class="fa-solid fa-user-plus"></i>  Follow'
 			this.className = 'btn btn-primary';
 		}
 		else {
 			numFollow += 1;
 			this.dataset.following = 'True';
 			this.innerHTML = '<i class="fa-solid fa-user-large-slash"></i> Unfollow'
 			this.className = 'btn btn-danger';
 		}
 		numFollowers.innerHTML = numFollow;
 		follow(user2);
 		console.log(user2);
 		//follow this person
 		//(send info to server)
 		}
 	};

 	//select delete button
 	const deleteButton = document.querySelectorAll('.trashcan');
 	if (deleteButton) {
 		deleteButton.forEach(button => {
 			button.onclick = () => {
 				//get post id
 				const postId = button.dataset.postid;

 				//find parent post.
 				const post = button.parentElement.parentElement.parentElement.parentElement;
 				const modal = document.querySelector('#myModal')
 				modal.style.display = 'block';

				// Get the <span> element that closes the modal
				const close = document.querySelector("#close");

				const yes = document.querySelector("#yesButton");
				const no = document.querySelector("#noButton");

				// When the user clicks on <span> (x), close the modal
				close.onclick = function() {
				  modal.style.display = "none";
				}

				// When the user clicks anywhere outside of the modal, close it
				window.onclick = function(event) {
				  if (event.target == modal) {
				    modal.style.display = "none";
				  }
				}

				no.onclick = function() {
				modal.style.display = "none";

				}
				yes.onclick = function() {
					
					//do the rest here
					modal.style.display = "none";
					post.parentElement.removeChild(post);
 					//send info to server
 					deletePost(postId);

				}

		 	}

 		})

 	};

 	const comments = document.querySelectorAll('comments');
 	if (comments) {
 		//execute code
 		//display = none or removechild
 		//find parent post.
 		//find parent post container
 		//parent post container removechild(parentpost)
 	}

 } );


