import React from "react";
import { randomAvatar } from "../utils";
import { Navbar, Container, Image, NavDropdown, Nav } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { getUser } from "../hooks/user.actions";
import { Link } from "react-router-dom";
import useSWR from "swr";
import { fetcher } from "../helpers/axios";
import { UsergroupDeleteOutlined } from "@ant-design/icons";

function Navigationbar() {
  const navigate = useNavigate();
  const user = getUser();



  const handleLogout = () => {
    localStorage.removeItem("auth");
    navigate("/login/");
  };

  return (
    <Navbar bg="primary" variant="dark">
      <Container>
        <Navbar.Brand className="fw-bold" href="/">
          Posty
        </Navbar.Brand>
        <Navbar.Collapse className="justify-content-end">
          <Nav>
            <NavDropdown
              title={
                <Image
                  src={user.avatar}
                  roundedCircle
                  width={52}
                  height={52}
                  className="my-2"
                />
              }
            >
              <NavDropdown.Item as={Link} to={`/profile/${user.id}/`}>
                {" "}
                Profile{" "}
              </NavDropdown.Item>
              <NavDropdown.Item onClick={handleLogout}>Logout</NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
export default Navigationbar;
