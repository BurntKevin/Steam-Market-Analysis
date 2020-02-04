import React from 'react';
import Header from './Header';
import Body from './Body';

function Layout({ body, extraBody }) {
  return (
    <div style={{ display: 'inline' }}>
      <Header />
      <Body>{body}{extraBody}</Body>
    </div>
  );
}

export default Layout;
