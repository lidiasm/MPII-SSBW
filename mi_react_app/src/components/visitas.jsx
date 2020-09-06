import React, { Component } from "react";
import Visita from "./visita";

class Visitas extends Component {
  /**
   * Estado.
   *  - Array de visitas en el que se almacena la lista de visitas obtenidas de la API REST.
   *  - La visita seleccionada de la que mostrar la vista en detalle.
   */
  state = {
    visitas: [],
    comentarios: [],
    seleccionada: null,
  };

  /**
   * Función para recopilar las visitas de la base de datos utilizando la API REST.
   * Luego se almacenan en el estado para luego mostrarlas en la función render()
   */
  componentDidMount() {
    fetch("http://localhost:8000/visitas_granada/api/visitas")
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        this.setState({ visitas: data });
      })
      .catch((error) => {
        console.log(error);
      });

    fetch("http://localhost:8000/visitas_granada/api/comentarios")
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        this.setState({ comentarios: data });
      })
      .catch((error) => {
        console.log(error);
      });
  }

  /**
   * Función para actualizar el contador de likes tras pulsar uno
   * de los dos botones que suman y restan likes, respectivamente.
   * @param {*} visita la visita a la que modificar el número de likes.
   * @param {*} suma true si se aumenta el número de likes, false si se disminuyen.
   */
  actualizarLikes = (visita, suma) => {
    // Sumamos o restamos un like a la visita
    if (suma) {
      visita.likes += 1;
    } else {
      visita.likes -= 1;
    }
    // Actualizamos el nuevo contador de likes a la visita
    // almacenada en el estado
    this.setState({ seleccionada: visita });

    // Mandamos los datos como un JSON para actualizar la base de datos
    // utilizando la API REST del backend
    let json_likes = { likes: this.state.seleccionada.likes };
    fetch("http://localhost:8000/visitas_granada/api/likes/" + visita.id, {
      method: "PUT",
      body: JSON.stringify(json_likes),
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        console.log("Likes: ", data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  /**
   * Función de renderizado para mostrar tanto la página principal, en caso
   * de que no se haya seleccionado ninguna visita. O la vista en detalle de la
   * visita seleccionada.
   */
  render() {
    // Obtenemos el número de visitas para mostrarlas en la cabecera de la página
    let n_visitas = this.state.visitas.length;

    // Mostramos la vista en detalle si ya se ha seleccionado una de las visitas
    if (this.state.seleccionada != null) {
      return (
        <div className="container-sm">
          <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div
              className="collapse navbar-collapse"
              id="navbarSupportedContent"
            >
              <ul className="navbar-nav mr-auto">
                <li className="nav-item active">
                  <a
                    className="nav-link"
                    style={{ fontWeight: "bold" }}
                    href="index"
                  >
                    Inicio
                  </a>
                </li>
              </ul>
            </div>
          </nav>
          <div
            id="cabecera"
            style={{ background: "lightgrey", padding: 30, marginBottom: 20 }}
            className="header"
          >
            <h1>Visitas en Granada</h1>
            <h4>Tenemos {n_visitas} visitas</h4>
          </div>
          <div className="row">
            <div className="col-3"></div>
            <div className="col-9">
              <Visita
                key={this.state.seleccionada.id}
                visita={this.state.seleccionada}
                comentarios={this.state.comentarios}
                onActualizarLikes={this.actualizarLikes}
              />
            </div>
          </div>
        </div>
      );
    }
    // Vista de la página principal donde se muestran las tarjetas de las visitas
    // si no se ha seleccionado ninguna visita aún
    return (
      <div className="container-sm">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav mr-auto">
              <li className="nav-item active">
                <a
                  className="nav-link"
                  style={{ fontWeight: "bold" }}
                  href="index"
                >
                  Inicio
                </a>
              </li>
            </ul>
          </div>
        </nav>
        <div
          id="cabecera"
          style={{ background: "lightgrey", padding: 30 }}
          className="header"
        >
          <h1>Visitas en Granada</h1>
          <h4>Tenemos {n_visitas} visitas</h4>
        </div>

        <div className="row">
          <div className="col-3">
            <div
              id="menuLateral"
              className="sidenav block-example border border-dark"
              style={{
                height: "100%",
                borderRadius: "25px",
                marginTop: "20px",
                marginBottom: "20px",
              }}
            >
              <ul className="custom-scrollbar">
                <li>Menú lateral</li>
              </ul>
            </div>
          </div>

          <div className="col-9">
            {this.state.visitas.map((v) => (
              <div
                className="column"
                style={{ float: "left", width: "33%", padding: "0 10px" }}
                key={v.id}
              >
                <div style={{ marginTop: "20px" }} className="card h-100">
                  <img
                    style={{ height: "15vw", objectFit: "cover" }}
                    className="card-img-top img-thumbnail"
                    src={"http://localhost:8000" + v.foto}
                    alt={v.nombre}
                  ></img>
                  <h5
                    style={{ marginTop: "10px" }}
                    className="card-title text-center"
                  >
                    {v.nombre}
                  </h5>
                  <button
                    type="button"
                    onClick={() => this.setState({ seleccionada: v })}
                    className="btn btn-primary"
                  >
                    Detalles
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }
}

export default Visitas;
