import Table from 'react-bootstrap/Table';
import Pagination from 'react-bootstrap/Pagination';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useTable, usePagination, useGlobalFilter } from 'react-table';

const GlobalFilter = ({ globalFilter, setGlobalFilter }) => {
  const [value, setValue] = React.useState(globalFilter);
  const onChange = async value => setGlobalFilter(value || undefined);
  return (
    <Form.Control
      value={value || ''}
      placeholder="Search"
      onChange={e => {
        setValue(e.target.value);
        onChange(e.target.value);
      }}
    />
  );
};

export default ({ friendData }) => {
  const columns = React.useMemo(
    () => [
      {
        Header: 'Name',
        accessor: d =>
          d.last_name ? `${d.first_name} ${d.last_name}` : d.first_name,
      },
      {
        Header: 'Birthday',
        accessor: 'birthday',
      },
      {
        Header: 'Age',
        accessor: 'age',
      },
    ],
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    prepareRow,
    rows,
    page, // rows for the active page

    // global filtering helpers
    setGlobalFilter,

    // pagination helpers
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,
    // state variables
    state: { pageIndex, pageSize, globalFilter },
  } = useTable(
    {
      columns,
      data: friendData,
      initialState: { pageSize: 5 },
    },
    useGlobalFilter,
    usePagination
  );

  return (
    <>
      <Row className="justify-content-between">
        <Col>
          <Form.Control
            as="select"
            value={pageSize}
            onChange={e => setPageSize(Number(e.target.value))}
            style={{ width: 120 }}
          >
            {[5, 10, 20, 40].map(size => (
              <option key={size} value={size}>
                Show {size}
              </option>
            ))}
          </Form.Control>
        </Col>
        <Col xs={12} sm={6}>
          <GlobalFilter
            globalFilter={globalFilter}
            setGlobalFilter={setGlobalFilter}
          />
        </Col>
      </Row>

      <Table striped bordered hover {...getTableProps()}>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps()}>{column.render('Header')}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {page.map((row, i) => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map(cell => {
                  return (
                    <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </Table>

      <div className="d-flex justify-content-between">
        <Pagination>
          <Pagination.First
            onClick={() => gotoPage(0)}
            disabled={!canPreviousPage}
          />
          <Pagination.Prev
            onClick={() => previousPage()}
            disabled={!canPreviousPage}
          />
          <Pagination.Next onClick={() => nextPage()} disabled={!canNextPage} />
          <Pagination.Last
            onClick={() => gotoPage(pageCount - 1)}
            disabled={!canNextPage}
          />
        </Pagination>
        <div>
          Page {pageIndex + 1} of {pageOptions.length}{' '}
          <small className="text-muted">({rows.length} records)</small>
        </div>
        {/* <div>
          Showing {pageIndex * pageSize + 1} to {(1 + pageIndex) * pageSize} of{' '}
          {rows.length} records
        </div> */}
      </div>
    </>
  );
};
