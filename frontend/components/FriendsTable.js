import { useState } from 'react';
import Table from 'react-bootstrap/Table';
import Pagination from 'react-bootstrap/Pagination';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPen, faTrash } from '@fortawesome/free-solid-svg-icons';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useTable, usePagination, useGlobalFilter } from 'react-table';
import useAuth from 'contexts/auth';
import apiClient from 'services/api';
import { wait } from 'services/helpers';
import SubmitButton from 'components/widgets/SubmitButton';
import EditFriend from 'components/EditFriend';

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

export default ({ friends }) => {
  const { fetchUser } = useAuth();
  const [idDeleting, setIdDeleting] = useState(null);
  const [showEditForm, setShowEditForm] = useState(false);
  const [friendValues, setFriendValues] = useState(false);

  const deleteFriend = async id => {
    setIdDeleting(id);
    await wait(2000); // TODO: remove this
    const { error } = await apiClient.authenticatedDelete(`friends/${id}`);
    if (error) {
      console.log(error);
    } else {
      await fetchUser();
    }
    setIdDeleting(null);
  };

  const columns = React.useMemo(
    () => [
      {
        Header: 'Name',
        accessor: d =>
          d.last_name ? `${d.first_name} ${d.last_name}` : d.first_name,
      },
      {
        Header: 'Birthday',
        accessor: d => {
          const monthStr = d.birthday_month.toString().padStart(2, 0);
          const dayStr = d.birthday_day.toString().padStart(2, 0);
          return `${monthStr}-${dayStr}`;
        },
      },
      {
        Header: 'Age',
        accessor: 'age',
      },
      {
        id: 'actions',
        width: 115, // just large enough for 2 buttons with loading icon
        Header: '',
        Cell: ({ row: { original } }) => {
          const friend = {
            id: original.id,
            firstName: original.first_name,
            lastName: original.last_name,
            day: original.birthday_day,
            month: original.birthday_month,
            year: original.birthday_year,
          };
          return (
            <div>
              <Button
                onClick={() => {
                  setFriendValues(friend);
                  setShowEditForm(true);
                }}
                variant={'outline-secondary'}
                size={'sm'}
                title="Edit"
                style={{ marginRight: 10 }}
              >
                <FontAwesomeIcon icon={faPen} size={'sm'} />
              </Button>
              <SubmitButton
                onClick={() => deleteFriend(original.id)}
                isSubmitting={idDeleting === original.id}
                text={<FontAwesomeIcon icon={faTrash} size={'sm'} />}
                variant={'outline-danger'}
                size={'sm'}
                title="Delete"
              />
            </div>
          );
        },
      },
    ],
    [idDeleting]
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
      data: friends,
      initialState: { pageSize: 5 },
    },
    useGlobalFilter,
    usePagination
  );

  return (
    <>
      <h4>Friends</h4>

      <EditFriend
        show={showEditForm}
        setShow={setShowEditForm}
        friendValues={friendValues}
      />

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

      <Table striped bordered hover responsive {...getTableProps()}>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th
                  {...column.getHeaderProps()}
                  width={column.width !== 150 ? column.width : null}
                >
                  {column.render('Header')}
                </th>
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
      </div>
    </>
  );
};
