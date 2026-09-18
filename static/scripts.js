   async function getstudent(){
       const response= await fetch('/api/student')
       const info= await response.json()
       const nme=document.getElementById("sname")
       const clg=document.getElementById("scollege")
       const crs=document.getElementById("scourse")
       nme.textContent= info.name
       clg.textContent= info.college
       crs.textContent= info.course
    }
    getstudent()