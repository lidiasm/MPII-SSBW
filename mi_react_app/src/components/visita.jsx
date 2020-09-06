import React, { Component } from "react";

class Visita extends Component {
  /**
   * Función de renderizado que muestra la vista en detalle de una determinada visita.
   * También se le añaden los dos botones de "like" y "dislike" que actualizan tanto
   * la base de datos del backend como la vista en detalle de la visita en cuestión.
   */
  render() {
    // Primer argumento pasado como parámetro: la visita a mostrar en detalle
    let v = this.props.visita;
    // Segundo argumento pasado como parámetro: todos los comentarios
    let todos = this.props.comentarios;

    // Filtramos los comentarios por la visita a mostrar en detalle
    let comentarios_visita = [];
    todos.map(function (val) {
      if (v.id === val["visita"]) {
        comentarios_visita.push(val);
      }
    });
    // Si no hay comentarios para la visita, se lo hacemos saber al usuario
    if (comentarios_visita.length === 0) {
      comentarios_visita.push({
        id: 1,
        texto: "No hay comentarios disponibles",
      });
    }

    return (
      <div>
        <a
          href="index"
          style={{ float: "right" }}
          className="btn btn-secondary"
        >
          Volver
        </a>

        <h3>
          <strong>{v.nombre}</strong>
        </h3>
        <div className="row">
          <div className="col-3">
            <img
              style={{ width: "20px" }}
              src={"http://localhost:8000/media/fotos/like.jpeg"}
            ></img>
          </div>
          <div
            className="col-3"
            style={{ marginLeft: "-185px", marginTop: "2px" }}
          >
            <p id="likes" style={{ color: "#f04f64" }}>
              {v.likes}
            </p>
          </div>
          <div
            className="col"
            style={{ marginTop: "-5px", marginLeft: "-180px" }}
          >
            <button
              id="like"
              onClick={() => this.props.onActualizarLikes(v, true)}
              type="button"
              className="btn btn-default"
            >
              <i className="fa fa-thumbs-o-up"></i>
            </button>
            <button
              id="dislike"
              onClick={() => this.props.onActualizarLikes(v, false)}
              type="button"
              className="btn btn-default"
              style={{ marginLeft: "-10px" }}
            >
              <i className="fa fa-thumbs-o-down"></i>
            </button>
          </div>
        </div>
        <h5>{v.descripción}</h5>
        <p>
          <img
            className="img-thumbnail"
            style={{ width: "50%" }}
            src={"http://localhost:8000" + v.foto}
            alt={v.nombre}
          ></img>
        </p>
        <h4 style={{ marginTop: "40px" }}>Comentarios</h4>
        {comentarios_visita.map((c) => (
          <div className="card" id={c.id} style={{ margin: "15px" }}>
            <div className="card-body">{c.texto}</div>
          </div>
        ))}
      </div>
    );
  }
}

export default Visita;
