package main

import (
    "html/template"
    "fmt"
    "net/http"
    "io"
    "os"
)

type ReviewInfo struct {
    Id uint
    Author string
    Title string
    FilePaths []string
}

func main(){
    var next_id uint = 0
    var details_list []ReviewInfo

    new_review_tmpl := template.Must(template.ParseFiles("pages/new_review.html"))
    new_file_tmpl := template.Must(template.ParseFiles("pages/new_file.html"))
    details_tmpl := template.Must(template.ParseFiles("pages/review_details.html"))

    fs := http.FileServer(http.Dir("assets/"))
    http.Handle("/assets/", http.StripPrefix("/assets/", fs))

    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        if r.Method != http.MethodPost {
            new_review_tmpl.Execute(w, nil)
            return
        }

        details := ReviewInfo{
            Id: next_id,
            Author: r.FormValue("author"),
            Title: r.FormValue("title"),
        }
        next_id += 1

        fmt.Println(details)
        details_list = append(details_list, details)

        newUrl := fmt.Sprintf("/reviews/%v/addfile", details.Id)
        http.Redirect(w, r, newUrl, http.StatusSeeOther)
    })

    var id uint
    http.HandleFunc("/reviews/{id}/addfile", func(w http.ResponseWriter, r *http.Request) {
        details := details_list[id]

        if r.Method != http.MethodPost {
            new_file_tmpl.Execute(w, details)
            return
        }


        file, handler, err := r.FormFile("file")
        if err != nil {
            panic(err) //dont do this
        }
        defer file.Close()



        details.FilePaths = append(details.FilePaths, handler.Filename)
        details_list[id] = details
        fmt.Println(details, r.FormValue("file"))

        io.Copy(os.Stdout, file)

        new_file_tmpl.Execute(w, details)
    })

    http.HandleFunc("/reviews/{id}", func(w http.ResponseWriter, r *http.Request) {
        details := details_list[id]
        details_tmpl.Execute(w, details)
    })

    http.ListenAndServe(":8000", nil)
}
