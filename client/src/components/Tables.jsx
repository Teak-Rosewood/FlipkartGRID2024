import React from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    Typography,
    Table,
    TableHead,
    TableBody,
    TableRow,
    TableCell,
    TableContainer,
    Paper,
    Collapse,
    IconButton,
    Box,
} from '@mui/material';
import { KeyboardArrowDown, KeyboardArrowUp } from '@mui/icons-material';
import { useState } from 'react';

const CollapsibleTable = ({ title, data, columns }) => {
    const [open, setOpen] = useState(true);
    console.log(data)
    data.map((row, index) => (
        // console.log(row)

        columns.map((col) => (
            console.log(col),
            console.log(row[col])
        ))
    ))

    //   console.log(data.length)
    //   console.log(data[0].length)

    return (
        <Box mb={3}>
            <Box display="flex" alignItems="center">
                <IconButton size="small" onClick={() => setOpen(!open)}>
                    {open ? <KeyboardArrowUp /> : <KeyboardArrowDown />}
                </IconButton>
                <Typography
                    variant="h6"
                    sx={{ ml: 1, fontWeight: 'bold', color: '#ced4da' }}
                >
                    {title}
                </Typography>
            </Box>
            <Collapse in={open} timeout="auto" unmountOnExit>
                {data && data.length > 0 ? (
                    <TableContainer
                        component={Paper}
                        elevation={3}
                        sx={{ border: '1px solid #495057', borderRadius: '8px' }}
                    >
                        <Table size="small" sx={{ minWidth: 650 }}>
                            <TableHead>
                                <TableRow sx={{ bgcolor: '#495057' }}>
                                    {columns.map((column) => (
                                        <TableCell
                                            key={column}
                                            sx={{ fontWeight: 'bold', color: '#ced4da' }}
                                        >
                                            {column}
                                        </TableCell>
                                    ))}
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {data.map((row, index) => (
                                    <TableRow
                                        key={index}
                                        hover
                                        sx={{
                                            '&:nth-of-type(odd)': { backgroundColor: '#6c757d' },
                                            '&:nth-of-type(even)': { backgroundColor: '#6c757d' },
                                            '&:hover': { backgroundColor: '#495057' },
                                        }}
                                    >
                                        {columns.map((col) => (
                                            <TableCell
                                                key={col}
                                                sx={{ color: '#ced4da' }}
                                            >
                                                {typeof row[col] === 'object'
                                                ? JSON.stringify(row[col])
                                                : typeof row[col] === 'boolean'
                                                ? row[col].toString()
                                                : row[col]}
                                            </TableCell>
                                        ))}
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                ) : (
                    <Typography variant="body2" sx={{ ml: 4, color: '#757575' }}>
                        No data available.
                    </Typography>
                )}
            </Collapse>
        </Box>
    );
};

const EnhancedDialog = ({ isOpen, handleClose, allData }) => {
    const scanColumns = ['scan_id', 'timestamp', 'count', 'processed', 'items_detected'];
    const imageColumns = ['image_id', 'scan_id', 'timestamp', 'ocr_text'];
    const productColumns = [
        'product_id',
        'scan_id',
        'brand',
        'price',
        'expiry_date',
        'expired',
        'shelf_life',
        'summary',
    ];
    const freshColumns = [
        'product_id',
        'scan_id',
        'produce',
        'freshness',
        'shelf_life',
        'summary',
    ];

    return (
        <Dialog open={isOpen} onClose={handleClose} maxWidth="lg" fullWidth>
            <DialogTitle
                sx={{
                    fontWeight: 'bold',
                    bgcolor: '#212529',
                    color: 'white',
                }}
            >
                Database
            </DialogTitle>
            <DialogContent dividers sx={{ bgcolor: '#212529' }}>
                {allData ? (
                    <>
                        <CollapsibleTable
                            title="Scan Table"
                            data={allData.scan_data}
                            columns={scanColumns}
                        />
                        <CollapsibleTable
                            title="Image Data"
                            data={allData.image_data}
                            columns={imageColumns}
                        />
                        <CollapsibleTable
                            title="Product Data"
                            data={allData.product_data}
                            columns={productColumns}
                        />
                        <CollapsibleTable
                            title="Fresh Data"
                            data={allData.fresh_data}
                            columns={freshColumns}
                        />
                    </>
                ) : (
                    <Typography
                        variant="body1"
                        sx={{ color: '#b71c1c', textAlign: 'center', py: 2 }}
                    >
                        No data available.
                    </Typography>
                )}
            </DialogContent>
            <DialogActions sx={{ bgcolor: '#212529' }}>
                <Button
                    onClick={handleClose}
                    sx={{
                        color: '#212529',
                        fontWeight: 'bold',
                        '&:hover': { bgcolor: '#3949ab' },
                    }}
                    variant="contained"
                    color="primary"
                >
                    Close
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default EnhancedDialog;

