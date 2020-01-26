import React from 'react';
import Header from './Header';
import Body from './Body';

function Layout({ body }) {
  return (
    <div style={{ display: 'inline' }}>
      <Header />
      <Body>{body}</Body>
    </div>
  );
}

export default Layout;
