import React from "react";
import { Menu,  Container, Image } from "semantic-ui-react";

function Layout({ body, extraBody }) {
  return (
    <Container fluid>
      <Menu stackable>
        <Image src="logo.png" size="mini" />
      </Menu>

      <Container fluid>
        {body}
      </Container>
      <Container fluid>
        {extraBody}
      </Container>
    </Container>
  );
}

export default Layout;
